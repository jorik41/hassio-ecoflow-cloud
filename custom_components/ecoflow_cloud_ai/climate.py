from __future__ import annotations

from typing import Any

from homeassistant.components.climate import (
    ClimateEntity,
    ClimateEntityFeature,
    HVACMode,
)
from homeassistant.components.climate.const import (
    PRESET_ECO,
    PRESET_SLEEP,
    PRESET_NONE,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfTemperature, ATTR_TEMPERATURE
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import ECOFLOW_DOMAIN
from .api import EcoflowApiClient
from .devices import BaseDevice
from .entities import EcoFlowAbstractEntity


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    client: EcoflowApiClient = hass.data[ECOFLOW_DOMAIN][entry.entry_id]
    for device in client.devices.values():
        async_add_entities(device.climates(client))


class Wave2ClimateEntity(ClimateEntity, EcoFlowAbstractEntity):
    """Climate entity for Wave 2."""

    _attr_temperature_unit = UnitOfTemperature.CELSIUS
    _attr_target_temperature_step = 1
    _attr_min_temp = 16
    _attr_max_temp = 30
    _attr_hvac_modes = [HVACMode.OFF, HVACMode.COOL, HVACMode.HEAT, HVACMode.FAN_ONLY]
    _attr_fan_modes = ["Low", "Medium", "High"]
    _attr_preset_modes = [PRESET_NONE, PRESET_ECO, PRESET_SLEEP, "Max"]
    _attr_supported_features = (
        ClimateEntityFeature.TARGET_TEMPERATURE
        | ClimateEntityFeature.FAN_MODE
        | ClimateEntityFeature.PRESET_MODE
        | ClimateEntityFeature.TURN_ON
        | ClimateEntityFeature.TURN_OFF
    )

    def __init__(self, client: EcoflowApiClient, device: BaseDevice) -> None:
        super().__init__(client, device, "Air Conditioner", "climate")
        self._current_temperature: float | None = None
        self._target_temperature: float | None = None
        self._hvac_mode: HVACMode = HVACMode.OFF
        self._fan_mode: str = "Low"
        self._preset_mode: str = PRESET_NONE
        self._attr_available = True

    @property
    def current_temperature(self) -> float | None:
        return self._current_temperature

    @property
    def target_temperature(self) -> float | None:
        return self._target_temperature

    @property
    def hvac_mode(self) -> HVACMode:
        return self._hvac_mode

    @property
    def fan_mode(self) -> str | None:
        return self._fan_mode

    @property
    def preset_mode(self) -> str | None:
        return self._preset_mode

    def _handle_coordinator_update(self) -> None:
        if not self.coordinator.data.changed:
            return

        data = self.coordinator.data.data_holder.params
        if not data:
            return

        if "pd.envTemp" in data:
            self._current_temperature = float(data["pd.envTemp"])
        if "pd.setTemp" in data:
            self._target_temperature = float(data["pd.setTemp"])

        power_mode = data.get("pd.powerMode")
        power_status = data.get("pd.powerSts")
        run_status = data.get("pd.runSts")
        main_mode = data.get("pd.mainMode") or data.get("pd.pdMainMode")

        if power_status is not None:
            device_on = power_status == 1
        elif run_status is not None:
            device_on = run_status > 0
        elif power_mode is not None:
            device_on = power_mode == 1
        else:
            device_on = False

        if not device_on:
            self._hvac_mode = HVACMode.OFF
        else:
            if main_mode == 0:
                self._hvac_mode = HVACMode.COOL
            elif main_mode == 1:
                self._hvac_mode = HVACMode.HEAT
            elif main_mode == 2:
                self._hvac_mode = HVACMode.FAN_ONLY
            else:
                self._hvac_mode = HVACMode.OFF

        fan_value = data.get("pd.fanValue")
        if fan_value == 0:
            self._fan_mode = "Low"
        elif fan_value == 1:
            self._fan_mode = "Medium"
        elif fan_value == 2:
            self._fan_mode = "High"

        sub_mode = data.get("pd.pdSubMode") or data.get("pd.subMode")
        if sub_mode == 0:
            self._preset_mode = "Max"
        elif sub_mode == 1:
            self._preset_mode = PRESET_SLEEP
        elif sub_mode == 2:
            self._preset_mode = PRESET_ECO
        elif sub_mode == 3:
            self._preset_mode = PRESET_NONE
        else:
            self._preset_mode = PRESET_NONE

        self._attr_available = any(
            key in data for key in ["pd.setTemp", "pd.powerMode", "pd.envTemp", "pd.runSts", "pd.powerSts"]
        )
        self.schedule_update_ha_state()

    def _send_command(self, mqtt_key: str, value: Any, operate_type: str, param_name: str) -> None:
        command = {
            "moduleType": 1,
            "operateType": operate_type,
            "sn": self._device.device_info.sn,
            "params": {param_name: value},
        }
        adopted_key = f"'{mqtt_key}'" if self._device.flat_json() else mqtt_key
        self._client.send_set_message(self._device.device_info.sn, {adopted_key: value}, command)

    async def async_set_temperature(self, **kwargs: Any) -> None:
        if ATTR_TEMPERATURE in kwargs:
            temp = int(kwargs[ATTR_TEMPERATURE])
            self._send_command("pd.setTemp", temp, "setTemp", "setTemp")

    async def async_set_hvac_mode(self, hvac_mode: HVACMode) -> None:
        if hvac_mode == HVACMode.OFF:
            self._send_command("pd.powerMode", 2, "powerMode", "powerMode")
        else:
            self._send_command("pd.powerMode", 1, "powerMode", "powerMode")
            main_mode_val = 0
            if hvac_mode == HVACMode.HEAT:
                main_mode_val = 1
            elif hvac_mode == HVACMode.FAN_ONLY:
                main_mode_val = 2
            elif hvac_mode == HVACMode.COOL:
                main_mode_val = 0
            self._send_command("pd.mainMode", main_mode_val, "mainMode", "mainMode")

    async def async_set_fan_mode(self, fan_mode: str) -> None:
        fan_val = 0
        if fan_mode == "Medium":
            fan_val = 1
        elif fan_mode == "High":
            fan_val = 2
        self._send_command("pd.fanValue", fan_val, "fanValue", "fanValue")

    async def async_set_preset_mode(self, preset_mode: str) -> None:
        sub_mode_val = 3
        if preset_mode == "Max":
            sub_mode_val = 0
        elif preset_mode == PRESET_SLEEP:
            sub_mode_val = 1
        elif preset_mode == PRESET_ECO:
            sub_mode_val = 2
        self._send_command("pd.subMode", sub_mode_val, "subMode", "subMode")

    async def async_turn_on(self) -> None:
        self._send_command("pd.powerMode", 1, "powerMode", "powerMode")

    async def async_turn_off(self) -> None:
        self._send_command("pd.powerMode", 2, "powerMode", "powerMode")
