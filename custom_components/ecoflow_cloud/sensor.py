import enum
import logging
import struct
from typing import Any, Mapping, OrderedDict, override

import jsonpath_ng.ext as jp

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    PERCENTAGE,
    UnitOfElectricCurrent,
    UnitOfElectricPotential,
    UnitOfEnergy,
    UnitOfFrequency,
    UnitOfPower,
    UnitOfTemperature,
    UnitOfTime,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.util import dt

from . import (
    ATTR_MQTT_CONNECTED,
    ATTR_QUOTA_REQUESTS,
    ATTR_STATUS_DATA_LAST_UPDATE,
    ATTR_STATUS_PHASE,
    ATTR_STATUS_RECONNECTS,
    ATTR_STATUS_SN,
    ECOFLOW_DOMAIN,
)
from .api import EcoflowApiClient
from .devices import BaseDevice, const
from .entities import (
    BaseSensorEntity,
    EcoFlowAbstractEntity,
    EcoFlowDictEntity,
)
from .energy_store import EnergyStore

_LOGGER = logging.getLogger(__name__)


def _power_scale_for_sensor(sensor: BaseSensorEntity) -> float:
    """Return the scale factor for the given power sensor."""
    if isinstance(
        sensor,
        (
            DeciwattsSensorEntity,
            InWattsSolarSensorEntity,
            OutWattsDcSensorEntity,
        ),
    ):
        return 0.1
    if isinstance(sensor, InRawTotalWattsSolarSensorEntity):
        return 0.001
    return 1.0


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
):
    client: EcoflowApiClient = hass.data[ECOFLOW_DOMAIN][entry.entry_id]
    if "energy_store" not in hass.data[ECOFLOW_DOMAIN]:
        hass.data[ECOFLOW_DOMAIN]["energy_store"] = await EnergyStore.async_create(hass)
    store: EnergyStore = hass.data[ECOFLOW_DOMAIN]["energy_store"]
    for sn, device in client.devices.items():
        sensors = list(device.sensors(client))

        if device.device_info.device_type.upper() == "POWERSTREAM":
            sensors.append(
                DailyEnergySensorEntity(
                    client,
                    device,
                    ["254_32.watthPv1", "254_32.watthPv2"],
                    const.TOTAL_IN_ENERGY,
                    store,
                )
            )
            sensors.append(
                DailyEnergySensorEntity(
                    client,
                    device,
                    ["254_32.watthToBattery", "254_32.watthToSmartPlugs"],
                    const.TOTAL_OUT_ENERGY,
                    store,
                )
            )
            sensors.append(
                DailyEnergySensorEntity(
                    client,
                    device,
                    [
                        "254_32.watthPv1",
                        "254_32.watthPv2",
                        "254_32.watthFromBattery",
                        "254_32.watthToBattery",
                        "254_32.watthToSmartPlugs",
                    ],
                    const.TOTAL_ENERGY,
                    store,
                )
            )
            inv_power = next(
                (s for s in sensors if s.name == "Inverter Output Watts"),
                None,
            )
            if inv_power is not None:
                sensors.append(
                    CalculatedEnergySensorEntity(
                        client,
                        device,
                        inv_power.mqtt_key,
                        const.INVERTER_OUT_ENERGY,
                        store,
                        _power_scale_for_sensor(inv_power),
                    )
                )

        name_to_sensor = {s.name: s for s in sensors}

        energy_groups: dict[str, list[str]] = {
            const.TOTAL_IN_ENERGY: [const.TOTAL_IN_POWER],
            const.TOTAL_OUT_ENERGY: [const.TOTAL_OUT_POWER],
            const.TOTAL_ENERGY: [const.TOTAL_IN_POWER, const.TOTAL_OUT_POWER],
            const.AC_IN_ENERGY: [const.AC_IN_POWER],
            const.CHARGE_AC_ENERGY: [const.AC_IN_POWER],
            const.DISCHARGE_AC_ENERGY: [const.AC_OUT_POWER],
            const.SOLAR_IN_ENERGY: [
                const.SOLAR_IN_POWER,
                const.SOLAR_1_IN_POWER,
                const.SOLAR_2_IN_POWER,
            ],
            const.DISCHARGE_DC_ENERGY: [
                const.DC_OUT_POWER,
                const.DC_CAR_OUT_POWER,
                const.DC_ANDERSON_OUT_POWER,
                const.DC_12V_OUT_POWER,
                const.DC_24V_OUT_POWER,
            ],
            const.PV_HV_ENERGY: [const.PV_HV_POWER],
            const.POWER_INOUT_PORT_ENERGY: [const.POWER_INOUT_PORT],
            const.EXTRA_BATTERY_1_ENERGY: [const.EXTRA_BATTERY_1_OUT_POWER],
            const.EXTRA_BATTERY_2_ENERGY: [const.EXTRA_BATTERY_2_OUT_POWER],
            const.INVERTER_OUT_ENERGY: [const.AC_OUT_POWER],
            const.TYPEC_OUT_ENERGY: [
                const.TYPEC_OUT_POWER,
                const.TYPEC_1_OUT_POWER,
                const.TYPEC_2_OUT_POWER,
            ],
            const.USB_OUT_ENERGY: [
                const.USB_OUT_POWER,
                const.USB_1_OUT_POWER,
                const.USB_2_OUT_POWER,
                const.USB_3_OUT_POWER,
                const.USB_QC_1_OUT_POWER,
                const.USB_QC_2_OUT_POWER,
            ],
        }

        for energy_title, power_names in energy_groups.items():
            if any(s.name == energy_title for s in sensors):
                continue
            keys: list[str] = []
            scales: list[float] = []
            for name in power_names:
                sensor = name_to_sensor.get(name)
                if sensor is not None:
                    keys.append(sensor.mqtt_key)
                    scales.append(_power_scale_for_sensor(sensor))
            if keys:
                sensors.append(
                    CalculatedEnergySensorEntity(
                        client, device, keys, energy_title, store, scales
                    )
                )

        async_add_entities(sensors)


class MiscBinarySensorEntity(BinarySensorEntity, EcoFlowDictEntity):
    def _update_value(self, val: Any) -> bool:
        self._attr_is_on = bool(val)
        return True


class ChargingStateSensorEntity(BaseSensorEntity):
    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_icon = "mdi:battery-charging"
    _attr_device_class = BinarySensorDeviceClass.BATTERY_CHARGING

    def _update_value(self, val: Any) -> bool:
        if val == 0:
            return super()._update_value("unused")
        elif val == 1:
            return super()._update_value("charging")
        elif val == 2:
            return super()._update_value("discharging")
        else:
            return False


class CyclesSensorEntity(BaseSensorEntity):
    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_icon = "mdi:battery-heart-variant"
    _attr_state_class = SensorStateClass.TOTAL_INCREASING


class FanSensorEntity(BaseSensorEntity):
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_icon = "mdi:fan"


class MiscSensorEntity(BaseSensorEntity):
    _attr_entity_category = EntityCategory.DIAGNOSTIC


class LevelSensorEntity(BaseSensorEntity):
    _attr_device_class = SensorDeviceClass.BATTERY
    _attr_native_unit_of_measurement = PERCENTAGE
    _attr_state_class = SensorStateClass.MEASUREMENT


class RemainSensorEntity(BaseSensorEntity):
    _attr_device_class = SensorDeviceClass.DURATION
    _attr_native_unit_of_measurement = UnitOfTime.MINUTES
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_value = 0

    def _update_value(self, val: Any) -> Any:
        ival = int(val)
        if ival < 0 or ival > 5000:
            ival = 0

        return super()._update_value(ival)


class SecondsRemainSensorEntity(BaseSensorEntity):
    _attr_device_class = SensorDeviceClass.DURATION
    _attr_native_unit_of_measurement = UnitOfTime.SECONDS
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_value = 0

    def _update_value(self, val: Any) -> Any:
        ival = int(val)
        if ival < 0 or ival > 5000:
            ival = 0

        return super()._update_value(ival)


class TempSensorEntity(BaseSensorEntity):
    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_value = -1


class CelsiusSensorEntity(TempSensorEntity):
    def _update_value(self, val: Any) -> bool:
        return super()._update_value(int(val))


class DecicelsiusSensorEntity(TempSensorEntity):
    def _update_value(self, val: Any) -> bool:
        return super()._update_value(int(val) / 10)


class MilliCelsiusSensorEntity(TempSensorEntity):
    def _update_value(self, val: Any) -> bool:
        return super()._update_value(int(val) / 100)


class VoltSensorEntity(BaseSensorEntity):
    _attr_device_class = SensorDeviceClass.VOLTAGE
    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_native_unit_of_measurement = UnitOfElectricPotential.VOLT
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_value = 0


class MilliVoltSensorEntity(BaseSensorEntity):
    _attr_device_class = SensorDeviceClass.VOLTAGE
    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_native_unit_of_measurement = UnitOfElectricPotential.MILLIVOLT
    _attr_suggested_unit_of_measurement = UnitOfElectricPotential.VOLT
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_value = 3


class BeSensorEntity(BaseSensorEntity):
    def _update_value(self, val: Any) -> bool:
        return super()._update_value(
            int(struct.unpack("<I", struct.pack(">I", val))[0])
        )


class BeMilliVoltSensorEntity(BeSensorEntity):
    _attr_device_class = SensorDeviceClass.VOLTAGE
    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_native_unit_of_measurement = UnitOfElectricPotential.MILLIVOLT
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_value = 0


class DeciMilliVoltSensorEntity(MilliVoltSensorEntity):
    def _update_value(self, val: Any) -> bool:
        return super()._update_value(int(val) / 10)


class InMilliVoltSensorEntity(MilliVoltSensorEntity):
    _attr_icon = "mdi:transmission-tower-import"
    _attr_suggested_display_precision = 0


class OutMilliVoltSensorEntity(MilliVoltSensorEntity):
    _attr_icon = "mdi:transmission-tower-export"
    _attr_suggested_display_precision = 0


class DecivoltSensorEntity(BaseSensorEntity):
    _attr_device_class = SensorDeviceClass.VOLTAGE
    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_native_unit_of_measurement = UnitOfElectricPotential.VOLT
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_value = 0

    def _update_value(self, val: Any) -> bool:
        return super()._update_value(int(val) / 10)


class CentivoltSensorEntity(DecivoltSensorEntity):
    def _update_value(self, val: Any) -> bool:
        return super()._update_value(int(val) / 10)


class AmpSensorEntity(BaseSensorEntity):
    _attr_device_class = SensorDeviceClass.CURRENT
    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_native_unit_of_measurement = UnitOfElectricCurrent.AMPERE
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_value = 0


class MilliampSensorEntity(BaseSensorEntity):
    _attr_device_class = SensorDeviceClass.CURRENT
    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_native_unit_of_measurement = UnitOfElectricCurrent.MILLIAMPERE
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_value = 0


class DeciampSensorEntity(BaseSensorEntity):
    _attr_device_class = SensorDeviceClass.CURRENT
    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_native_unit_of_measurement = UnitOfElectricCurrent.AMPERE
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_value = 0

    def _update_value(self, val: Any) -> bool:
        return super()._update_value(int(val) / 10)


class WattsSensorEntity(BaseSensorEntity):
    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_device_class = SensorDeviceClass.POWER
    _attr_native_unit_of_measurement = UnitOfPower.WATT
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_value = 0


class EnergySensorEntity(BaseSensorEntity):
    _attr_device_class = SensorDeviceClass.ENERGY
    _attr_native_unit_of_measurement = UnitOfEnergy.WATT_HOUR
    _attr_state_class = SensorStateClass.TOTAL_INCREASING

    def _update_value(self, val: Any) -> bool:
        ival = int(val)
        if ival > 0:
            return super()._update_value(ival)
        else:
            return False


class BeEnergySensorEntity(BeSensorEntity, EnergySensorEntity):
    """Energy sensor with big-endian 32bit values."""


class InBeEnergySensorEntity(BeEnergySensorEntity):
    _attr_icon = "mdi:transmission-tower-import"


class OutBeEnergySensorEntity(BeEnergySensorEntity):
    _attr_icon = "mdi:transmission-tower-export"


class CapacitySensorEntity(BaseSensorEntity):
    _attr_native_unit_of_measurement = "mAh"
    _attr_state_class = SensorStateClass.MEASUREMENT


class CumulativeCapacitySensorEntity(CapacitySensorEntity):
    _attr_state_class = SensorStateClass.TOTAL_INCREASING

    def _update_value(self, val: Any) -> bool:
        ival = int(val)
        if ival > 0:
            return super()._update_value(ival)
        else:
            return False


class DeciwattsSensorEntity(WattsSensorEntity):
    def _update_value(self, val: Any) -> bool:
        return super()._update_value(int(val) / 10)


class InWattsSensorEntity(WattsSensorEntity):
    _attr_icon = "mdi:transmission-tower-import"


class InWattsSolarSensorEntity(InWattsSensorEntity):
    _attr_icon = "mdi:solar-power"

    def _update_value(self, val: Any) -> bool:
        return super()._update_value(int(val) / 10)


class InRawWattsSolarSensorEntity(InWattsSensorEntity):
    _attr_icon = "mdi:solar-power"


class InRawTotalWattsSolarSensorEntity(InRawWattsSolarSensorEntity):
    def _update_value(self, val: Any) -> bool:
        return super()._update_value(int(val) / 1000)


class InRawWattsAltSensorEntity(InWattsSensorEntity):
    _attr_icon = "mdi:engine"


class OutWattsSensorEntity(WattsSensorEntity):
    _attr_icon = "mdi:transmission-tower-export"


class OutWattsDcSensorEntity(WattsSensorEntity):
    _attr_icon = "mdi:transmission-tower-export"

    def _update_value(self, val: Any) -> bool:
        return super()._update_value(int(val) / 10)


class InVoltSensorEntity(VoltSensorEntity):
    _attr_icon = "mdi:transmission-tower-import"


class InVoltSolarSensorEntity(VoltSensorEntity):
    _attr_icon = "mdi:solar-power"

    def _update_value(self, val: Any) -> bool:
        return super()._update_value(int(val) / 10)


class OutVoltDcSensorEntity(VoltSensorEntity):
    _attr_icon = "mdi:transmission-tower-export"

    def _update_value(self, val: Any) -> bool:
        return super()._update_value(int(val) / 10)


class OutAmpSensorEntity(AmpSensorEntity):
    _attr_icon = "mdi:transmission-tower-export"


class InAmpSensorEntity(AmpSensorEntity):
    _attr_icon = "mdi:transmission-tower-import"


class OutMilliampSensorEntity(MilliampSensorEntity):
    _attr_icon = "mdi:transmission-tower-export"


class InMilliampSensorEntity(MilliampSensorEntity):
    _attr_icon = "mdi:transmission-tower-import"


class InMilliampSolarSensorEntity(MilliampSensorEntity):
    _attr_icon = "mdi:solar-power"

    def _update_value(self, val: Any) -> bool:
        return super()._update_value(int(val) * 10)


class InEnergySensorEntity(EnergySensorEntity):
    _attr_icon = "mdi:transmission-tower-import"


class OutEnergySensorEntity(EnergySensorEntity):
    _attr_icon = "mdi:transmission-tower-export"


class InEnergySolarSensorEntity(InEnergySensorEntity):
    _attr_icon = "mdi:solar-power"


class _ResettingMixin(EnergySensorEntity):
    @override
    def _update_value(self, val: Any) -> bool:
        # Skip the "if val == 0: False" logic
        return super(EnergySensorEntity, self)._update_value(val)


class ResettingInEnergySensorEntity(_ResettingMixin, InEnergySensorEntity):
    pass


class ResettingInEnergySolarSensorEntity(_ResettingMixin, InEnergySolarSensorEntity):
    pass


class ResettingOutEnergySensorEntity(_ResettingMixin, OutEnergySensorEntity):
    pass


class CalculatedEnergySensorEntity(BaseSensorEntity):
    """Energy sensor calculated from power values."""

    _attr_device_class = SensorDeviceClass.ENERGY
    _attr_native_unit_of_measurement = UnitOfEnergy.KILO_WATT_HOUR
    _attr_state_class = SensorStateClass.TOTAL_INCREASING

    def __init__(
        self,
        client: EcoflowApiClient,
        device: BaseDevice,
        mqtt_keys: str | list[str],
        title: str,
        store: "EnergyStore",
        scales: float | list[float] | None = None,
    ) -> None:
        if isinstance(mqtt_keys, str):
            keys = [mqtt_keys]
        else:
            keys = mqtt_keys
        unique_key = title.replace(" ", "_")
        super().__init__(client, device, unique_key, title, True)
        self._keys = [jp.parse(self._adopt_json_key(k)) for k in keys]
        if scales is None:
            self._scales = [1.0] * len(self._keys)
        elif isinstance(scales, (int, float)):
            self._scales = [float(scales)] * len(self._keys)
        else:
            self._scales = [float(s) for s in scales]
        self._store = store
        self._store_key = f"{device.device_data.sn}:{title}"
        data = self._store.get(self._store_key, {"value": 0.0, "time": None})
        self._attr_native_value = data.get("value", 0.0)
        self._last_time = (
            dt.parse_datetime(data["time"]) if data.get("time") is not None else None
        )
        self._attr_extra_state_attributes = {"source": "calculated"}

    def _handle_coordinator_update(self) -> None:
        params = self.coordinator.data.data_holder.params
        total = 0.0
        found = False
        for expr, scale in zip(self._keys, self._scales):
            values = expr.find(params)
            if len(values) == 1:
                total += float(values[0].value) * scale
                found = True
        if not found:
            return
        now = dt.utcnow()
        if self._last_time is not None:
            dt_seconds = (now - self._last_time).total_seconds()
            if dt_seconds > 0:
                self._attr_native_value = round(
                    self._attr_native_value + (total * dt_seconds) / 3600000,
                    5,
                )
        self._last_time = now
        self._store.set(
            self._store_key,
            {"value": self._attr_native_value, "time": now.isoformat()},
        )
        self.schedule_update_ha_state()


class DailyEnergySensorEntity(BaseSensorEntity):
    """Energy sensor calculated from daily counter values."""

    # Ignore spikes that imply an average power higher than this value (kW)
    max_avg_power_kw: float = 50.0

    _attr_device_class = SensorDeviceClass.ENERGY
    _attr_native_unit_of_measurement = UnitOfEnergy.KILO_WATT_HOUR
    _attr_state_class = SensorStateClass.TOTAL_INCREASING

    def __init__(
        self,
        client: EcoflowApiClient,
        device: BaseDevice,
        mqtt_keys: list[str],
        title: str,
        store: "EnergyStore",
    ) -> None:
        # Use title as unique key to avoid collisions with other sensors
        unique_key = title.replace(" ", "_")
        super().__init__(client, device, unique_key, title, True)
        self._keys = [jp.parse(self._adopt_json_key(k)) for k in mqtt_keys]
        self._store = store
        self._store_key = f"{device.device_data.sn}:{title}"
        data = self._store.get(
            self._store_key, {"value": 0.0, "counter": 0.0, "time": None}
        )
        self._attr_native_value = data.get("value", 0.0)
        self._last_counter = float(data.get("counter", 0.0))
        self._last_update = (
            dt.parse_datetime(data.get("time")) if data.get("time") else None
        )
        self._attr_extra_state_attributes = {"source": "daily"}

    def _handle_coordinator_update(self) -> None:
        params = self.coordinator.data.data_holder.params
        total = 0.0
        found = False
        for expr in self._keys:
            values = expr.find(params)
            if len(values) == 1:
                total += float(values[0].value)
                found = True
        if not found:
            return

        now = dt.utcnow()
        diff = total - self._last_counter
        if diff < 0:
            if self._last_update and now.date() != self._last_update.date():
                _LOGGER.info("day counter reset detected for %s", self.name)
                diff = total
            else:
                _LOGGER.debug(
                    "ignoring unexpected counter decrease for %s: %s -> %s",
                    self.name,
                    self._last_counter,
                    total,
                )
                return
        elif self._last_update:
            dt_hours = (now - self._last_update).total_seconds() / 3600
            if dt_hours > 0 and diff / 1000 > dt_hours * self.max_avg_power_kw:
                _LOGGER.debug(
                    "ignoring unrealistic counter jump for %s: %.2f kWh over %.2f h",
                    self.name,
                    diff / 1000,
                    dt_hours,
                )
                return

        if diff != 0:
            self._attr_native_value = round(self._attr_native_value + diff / 1000, 5)
            self._store.set(
                self._store_key,
                {
                    "value": self._attr_native_value,
                    "counter": total,
                    "time": now.isoformat(),
                },
            )
            self._last_counter = total
            self._last_update = now
            self.schedule_update_ha_state()


class FrequencySensorEntity(BaseSensorEntity):
    _attr_device_class = SensorDeviceClass.FREQUENCY
    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_native_unit_of_measurement = UnitOfFrequency.HERTZ
    _attr_state_class = SensorStateClass.MEASUREMENT


class DecihertzSensorEntity(FrequencySensorEntity):
    def _update_value(self, val: Any) -> bool:
        return super()._update_value(int(val) / 10)


class _OnlineStatus(enum.Enum):
    UNKNOWN = enum.auto()
    ASSUME_OFFLINE = enum.auto()
    OFFLINE = enum.auto()
    ONLINE = enum.auto()


class StatusSensorEntity(SensorEntity, EcoFlowAbstractEntity):
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    offline_barrier_sec: int = 120  # 2 minutes

    def __init__(
        self,
        client: EcoflowApiClient,
        device: BaseDevice,
        title: str = "Status",
        key: str = "status",
    ):
        super().__init__(client, device, title, key)
        self._attr_force_update = False

        self._online = _OnlineStatus.UNKNOWN
        self._last_update = dt.utcnow().replace(
            year=2000, month=1, day=1, hour=0, minute=0, second=0
        )
        self._skip_count = 0
        self._offline_skip_count = int(
            self.offline_barrier_sec / self.coordinator.update_interval.seconds
        )
        self._attrs = OrderedDict[str, Any]()
        self._attrs[ATTR_STATUS_SN] = self._device.device_info.sn
        self._attrs[ATTR_STATUS_DATA_LAST_UPDATE] = None
        self._attrs[ATTR_MQTT_CONNECTED] = None

    def _handle_coordinator_update(self) -> None:
        changed = False
        update_time = self.coordinator.data.data_holder.last_received_time()
        if self._last_update < update_time:
            self._last_update = max(update_time, self._last_update)
            self._skip_count = 0
            self._actualize_attributes()
            changed = True
        else:
            self._skip_count += 1

        changed = self._actualize_status() or changed

        if changed:
            self.schedule_update_ha_state()

    def _actualize_status(self) -> bool:
        changed = False
        if self._skip_count == 0:
            status = self.coordinator.data.data_holder.status.get("status")
            if status == 0 and self._online != _OnlineStatus.OFFLINE:
                self._online = _OnlineStatus.OFFLINE
                self._attr_native_value = "offline"
                self._actualize_attributes()
                changed = True
            elif status == 1 and self._online != _OnlineStatus.ONLINE:
                self._online = _OnlineStatus.ONLINE
                self._attr_native_value = "online"
                self._actualize_attributes()
                changed = True
        elif (
            self._online not in {_OnlineStatus.OFFLINE, _OnlineStatus.ASSUME_OFFLINE}
            and self._skip_count >= self._offline_skip_count
        ):
            self._online = _OnlineStatus.ASSUME_OFFLINE
            self._attr_native_value = "assume_offline"
            self._actualize_attributes()
            changed = True
        return changed

    def _actualize_attributes(self):
        if self._online in {_OnlineStatus.OFFLINE, _OnlineStatus.ONLINE}:
            self._attrs[ATTR_STATUS_DATA_LAST_UPDATE] = (
                f"< {self.offline_barrier_sec} sec"
            )
        else:
            self._attrs[ATTR_STATUS_DATA_LAST_UPDATE] = self._last_update

        self._attrs[ATTR_MQTT_CONNECTED] = self._client.mqtt_client.is_connected()

    @property
    def extra_state_attributes(self) -> Mapping[str, Any] | None:
        return self._attrs


class QuotaStatusSensorEntity(StatusSensorEntity):
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    def __init__(
        self,
        client: EcoflowApiClient,
        device: BaseDevice,
        title: str = "Status",
        key: str = "status",
    ):
        super().__init__(client, device, title, key)
        self._attrs[ATTR_QUOTA_REQUESTS] = 0

    def _actualize_status(self) -> bool:
        changed = False
        if (
            self._online != _OnlineStatus.ASSUME_OFFLINE
            and self._skip_count >= self._offline_skip_count * 2
        ):
            self._online = _OnlineStatus.ASSUME_OFFLINE
            self._attr_native_value = "assume_offline"
            self._attrs[ATTR_MQTT_CONNECTED] = self._client.mqtt_client.is_connected()
            changed = True
        elif (
            self._online != _OnlineStatus.ASSUME_OFFLINE
            and self._skip_count >= self._offline_skip_count
        ):
            self.hass.async_create_background_task(
                self._client.quota_all(self._device.device_info.sn), "get quota"
            )
            self._attrs[ATTR_QUOTA_REQUESTS] = self._attrs[ATTR_QUOTA_REQUESTS] + 1
            changed = True
        elif self._online != _OnlineStatus.ONLINE and self._skip_count == 0:
            self._online = _OnlineStatus.ONLINE
            self._attr_native_value = "online"
            self._attrs[ATTR_MQTT_CONNECTED] = self._client.mqtt_client.is_connected()
            changed = True
        return changed


class QuotaScheduledStatusSensorEntity(QuotaStatusSensorEntity):
    def __init__(
        self, client: EcoflowApiClient, device: BaseDevice, reload_delay: int = 3600
    ):
        super().__init__(client, device, "Status (Scheduled)", "status.scheduled")
        self.offline_barrier_sec: int = reload_delay
        self._quota_last_update = dt.utcnow()

    def _actualize_status(self) -> bool:
        changed = super()._actualize_status()
        quota_diff = dt.as_timestamp(dt.utcnow()) - dt.as_timestamp(
            self._quota_last_update
        )
        # if delay passed, reload quota
        if quota_diff > (self.offline_barrier_sec):
            self._attr_native_value = "updating"
            self._quota_last_update = dt.utcnow()
            self.hass.async_create_background_task(
                self._client.quota_all(self._device.device_info.sn), "get quota"
            )
            self._attrs[ATTR_QUOTA_REQUESTS] = self._attrs[ATTR_QUOTA_REQUESTS] + 1
            _LOGGER.debug("Reload quota for device %s", self._device.device_info.sn)
            changed = True
        else:
            if self._attr_native_value == "updating":
                changed = True
            self._attr_native_value = "online"
        return changed


class ReconnectStatusSensorEntity(StatusSensorEntity):
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    CONNECT_PHASES = [3, 5, 7]

    def __init__(self, client: EcoflowApiClient, device: BaseDevice):
        super().__init__(client, device)
        self._attrs[ATTR_STATUS_PHASE] = 0
        self._attrs[ATTR_STATUS_RECONNECTS] = 0

    def _actualize_status(self) -> bool:
        time_to_reconnect = self._skip_count in self.CONNECT_PHASES

        if self._online == _OnlineStatus.ONLINE and time_to_reconnect:
            self._attrs[ATTR_STATUS_RECONNECTS] = (
                self._attrs[ATTR_STATUS_RECONNECTS] + 1
            )
            self._client.mqtt_client.reconnect()
            return True
        else:
            return super()._actualize_status()
