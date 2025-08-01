from __future__ import annotations
import logging
from copy import deepcopy
from typing import Any, Dict

import voluptuous as vol
from homeassistant.config_entries import (
    ConfigEntry,
    ConfigFlow,
    OptionsFlowWithConfigEntry,
)
from homeassistant.core import callback
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers import selector
from homeassistant.helpers.device_registry import DeviceRegistry
from homeassistant.helpers.entity_registry import EntityRegistry

from . import (
    CONF_ACCESS_KEY,
    CONF_API_HOST,
    CONF_DEVICE_ID,
    CONF_DEVICE_LIST,
    CONF_DEVICE_NAME,
    CONF_DEVICE_TYPE,
    CONF_GROUP,
    CONF_PARENT_SN,
    CONF_PASSWORD,
    CONF_SECRET_KEY,
    CONF_SELECT_DEVICE_KEY,
    CONF_USERNAME,
    CONFIG_VERSION,
    DEFAULT_REFRESH_PERIOD_SEC,
    ECOFLOW_DOMAIN,
    OPTS_DIAGNOSTIC_MODE,
    OPTS_POWER_STEP,
    OPTS_REFRESH_PERIOD_SEC,
    CONF_LOCAL_MQTT_ENABLED,
    CONF_LOCAL_MQTT_HOST,
    CONF_LOCAL_MQTT_PORT,
    CONF_LOCAL_MQTT_SSL,
    CONF_INTERACTION_LOG_ENABLED,
    DeviceData,
    DeviceOptions,
    extract_devices,
)
from .api import EcoflowException
from .devices import EcoflowDeviceInfo

_LOGGER = logging.getLogger(__name__)

API_SELECT_DEVICE_SCHEMA = vol.Schema({vol.Required(CONF_SELECT_DEVICE_KEY): str})


class EcoflowConfigFlow(ConfigFlow, domain=ECOFLOW_DOMAIN):
    VERSION = CONFIG_VERSION

    def __init__(self) -> None:
        self.auth = None
        self.config_entry: ConfigEntry | None = None
        self.new_data = {}
        self.new_options = {}

        self.cloud_device = None
        self.cloud_devices: dict[str, EcoflowDeviceInfo] = {}
        self.local_devices: dict[str, DeviceData] = {}
        self._auth_type = None

    def set_current_config_entry(self, config_entry: ConfigEntry) -> None:
        self.config_entry = config_entry
        self.new_data = deepcopy(dict(config_entry.data))
        self.new_options = deepcopy(dict(config_entry.options))

    def set_device_list(self, device_list: list[EcoflowDeviceInfo]) -> None:
        for device in device_list:
            self.cloud_devices[f"{device.name} ({device.device_type})"] = device

    def set_local_device_list(self, devices: list[DeviceData]) -> None:
        for device in devices:
            self.local_devices[f"{device.name} ({device.sn})"] = device

    async def update_or_create(self):
        if self.config_entry:
            _LOGGER.info(
                ".. reconfigure: entry = %s, data = %s, options = %s ",
                str(self.config_entry),
                str(self.new_data),
                str(self.new_options),
            )
            if self.hass.config_entries.async_update_entry(
                entry=self.config_entry, data=self.new_data, options=self.new_options
            ):
                # reload if changed
                self.hass.config_entries.async_schedule_reload(
                    self.config_entry.entry_id
                )

            return self.async_abort(reason="reconfigure_successful")

        else:
            _LOGGER.info(
                ".. create: entry = %s, data = %s, options = %s ",
                str(self.config_entry),
                str(self.new_data),
                str(self.new_options),
            )

            from .devices.registry import device_support_sub_devices

            for sn, device_data in self.new_data[CONF_DEVICE_LIST].items():
                if device_data[CONF_DEVICE_TYPE] not in device_support_sub_devices:
                    # skip here all devices that do not support sub devices
                    continue
                from .api.public_api import EcoflowPublicApiClient

                if not isinstance(self.auth, EcoflowPublicApiClient):
                    raise TypeError(
                        "Only public api is supported for devices with sub devices"
                    )
                all_device_info = await self.auth.call_api(
                    "/device/quota/all", {"sn": sn}
                )
                for sub_device_type, sub_devices in all_device_info["data"].items():
                    if not isinstance(sub_devices, dict):
                        continue
                    for sub_device_sn, item in sub_devices.items():
                        if not isinstance(item, (dict, list)):
                            # skip all element that are simple
                            continue
                        self.new_data[CONF_DEVICE_LIST][sub_device_sn] = {
                            CONF_DEVICE_NAME: f"{device_data[CONF_DEVICE_NAME]}.{sub_device_type}.{sub_device_sn}",
                            CONF_DEVICE_TYPE: sub_device_type,
                            CONF_PARENT_SN: sn,
                        }
                        self.new_options[CONF_DEVICE_LIST][sub_device_sn] = (
                            self.new_options[CONF_DEVICE_LIST][sn]
                        )

            return self.async_create_entry(
                title=self.new_data[CONF_GROUP],
                data=self.new_data,
                options=self.new_options,
            )

    def remove_device(self, sn: str):
        # Get the device registry
        device_reg: DeviceRegistry = dr.async_get(self.hass)

        if CONF_ACCESS_KEY in self.config_entry.data:
            identifiers = {(ECOFLOW_DOMAIN, f"api-{sn}")}
        else:
            identifiers = {(ECOFLOW_DOMAIN, f"{sn}")}

        device = device_reg.async_get_device(identifiers=identifiers)
        _LOGGER.debug(".. getting device by %s: %s", str(identifiers), str(device))

        # Remove all entities for this device
        if getattr(device, "id", None) is not None:
            ent_reg: EntityRegistry = er.async_get(self.hass)
            entities = er.async_entries_for_device(ent_reg, device.id)

            for entity in entities:
                ent_reg.async_remove(entity.entity_id)

            # Remove the device from the device registry
            device_reg.async_remove_device(device.id)

    async def async_step_user(self, user_input: dict[str, Any] | None = None):
        if self.config_entry:  # reconfigure flow
            return await self.async_step_choose_type()

        if not user_input:
            return self.async_show_form(
                step_id="user",
                data_schema=vol.Schema(
                    {
                        vol.Required(
                            CONF_GROUP, default=self.new_data.get(CONF_GROUP, "Home")
                        ): str
                    }
                ),
            )

        self.new_data[CONF_GROUP] = user_input.get(CONF_GROUP)
        existing_entry = await self.async_set_unique_id(
            "group-" + self.new_data[CONF_GROUP], raise_on_progress=False
        )

        if existing_entry:
            return self.async_abort(reason="do_reconfigure_existing")

        return await self.async_step_choose_type()

    async def async_step_reconfigure(self, user_input: dict[str, Any] | None = None):
        self.set_current_config_entry(
            self.hass.config_entries.async_get_entry(self.context["entry_id"])
        )
        return await self.async_step_user()

    async def async_step_choose_type(self, user_input: dict[str, Any] | None = None):
        if self.config_entry:  # reconfig flow
            if CONF_ACCESS_KEY in self.config_entry.data:
                return await self.async_step_api()
            else:
                return await self.async_step_manual()

        if not user_input:
            return self.async_show_menu(
                step_id="choose_type", menu_options=["api", "manual"]
            )

    async def async_step_manual(self, user_input: dict[str, Any] | None = None):
        user_auth_schema = vol.Schema(
            {
                vol.Required(CONF_API_HOST, default="api.ecoflow.com"): str,
                vol.Required(
                    CONF_USERNAME, default=self.new_data.get(CONF_USERNAME, "")
                ): str,
                vol.Required(
                    CONF_PASSWORD, default=self.new_data.get(CONF_PASSWORD, "")
                ): str,
            }
        )

        if not user_input:
            return self.async_show_form(step_id="manual", data_schema=user_auth_schema)

        self.new_data[CONF_API_HOST] = user_input.get(CONF_API_HOST)
        self.new_data[CONF_USERNAME] = user_input.get(CONF_USERNAME)
        self.new_data[CONF_PASSWORD] = user_input.get(CONF_PASSWORD)

        from .api.private_api import EcoflowPrivateApiClient

        self.auth = EcoflowPrivateApiClient(
            self.new_data[CONF_API_HOST],
            self.new_data[CONF_USERNAME],
            self.new_data[CONF_PASSWORD],
            self.new_data[CONF_GROUP],
        )
        self._auth_type = "manual"

        errors: Dict[str, str] = {}
        try:
            await self.auth.login()
        except EcoflowException as e:  # pylint: disable=broad-except
            errors["base"] = str(e)
        except Exception:  # pylint: disable=broad-except
            _LOGGER.exception("Unexpected exception in login action")
            return self.async_abort(reason="unknown")

        if errors:
            return self.async_show_form(
                step_id="manual", data_schema=user_auth_schema, errors=errors
            )

        if self.config_entry:  # reconfig flow
            devices = extract_devices(self.config_entry)
            self.set_local_device_list(list(devices.values()))

            return self.async_show_menu(
                step_id="manual",
                menu_options=[
                    "manual_add_device",
                    "remove_device",
                    "mqtt",
                    "interaction_log",
                    "finish",
                ],
            )
        else:
            return await self.async_step_mqtt()

    async def async_step_manual_add_device(
        self, user_input: dict[str, Any] | None = None
    ):
        return await self.async_step_manual_device_input()

    async def async_step_manual_device_input(
        self, user_input: dict[str, Any] | None = None
    ):
        from .devices.registry import devices

        if not user_input:
            device_list = list(devices.keys())
            device_list.remove("DIAGNOSTIC")
            return self.async_show_form(
                step_id="manual_device_input",
                data_schema=vol.Schema(
                    {
                        vol.Required(CONF_DEVICE_TYPE): selector.SelectSelector(
                            selector.SelectSelectorConfig(
                                options=device_list,
                                mode=selector.SelectSelectorMode.DROPDOWN,
                            ),
                        ),
                        vol.Required(CONF_DEVICE_NAME): str,
                        vol.Required(CONF_DEVICE_ID): str,
                    }
                ),
            )

        device = devices[user_input[CONF_DEVICE_TYPE]]

        sn = user_input[CONF_DEVICE_ID]
        if CONF_DEVICE_LIST not in self.new_data:
            self.new_data[CONF_DEVICE_LIST] = {}
            self.new_options[CONF_DEVICE_LIST] = {}

        self.new_data[CONF_DEVICE_LIST][sn] = {
            CONF_DEVICE_NAME: user_input[CONF_DEVICE_NAME],
            CONF_DEVICE_TYPE: user_input[CONF_DEVICE_TYPE],
        }
        self.new_options[CONF_DEVICE_LIST][sn] = {
            OPTS_REFRESH_PERIOD_SEC: DEFAULT_REFRESH_PERIOD_SEC,
            OPTS_POWER_STEP: device.default_charging_power_step(),
            OPTS_DIAGNOSTIC_MODE: False,
        }

        return await self.update_or_create()

    async def async_step_mqtt(self, user_input: dict[str, Any] | None = None):
        schema = vol.Schema(
            {
                vol.Required(
                    CONF_LOCAL_MQTT_ENABLED,
                    default=self.new_data.get(CONF_LOCAL_MQTT_ENABLED, False),
                ): bool,
                vol.Optional(
                    CONF_LOCAL_MQTT_HOST,
                    default=self.new_data.get(CONF_LOCAL_MQTT_HOST, ""),
                ): str,
                vol.Optional(
                    CONF_LOCAL_MQTT_PORT,
                    default=self.new_data.get(CONF_LOCAL_MQTT_PORT, 1883),
                ): int,
                vol.Optional(
                    CONF_LOCAL_MQTT_SSL,
                    default=self.new_data.get(CONF_LOCAL_MQTT_SSL, False),
                ): bool,
            }
        )

        if user_input is None:
            return self.async_show_form(step_id="mqtt", data_schema=schema)

        self.new_data[CONF_LOCAL_MQTT_ENABLED] = user_input[CONF_LOCAL_MQTT_ENABLED]
        self.new_data[CONF_LOCAL_MQTT_HOST] = user_input.get(CONF_LOCAL_MQTT_HOST, "")
        self.new_data[CONF_LOCAL_MQTT_PORT] = user_input.get(CONF_LOCAL_MQTT_PORT, 1883)
        self.new_data[CONF_LOCAL_MQTT_SSL] = user_input.get(CONF_LOCAL_MQTT_SSL, False)

        if self.config_entry:
            return await self.update_or_create()

        return await self.async_step_interaction_log()

    async def async_step_interaction_log(
        self, user_input: dict[str, Any] | None = None
    ):
        schema = vol.Schema(
            {
                vol.Required(
                    CONF_INTERACTION_LOG_ENABLED,
                    default=self.new_data.get(CONF_INTERACTION_LOG_ENABLED, False),
                ): bool,
            }
        )

        if user_input is None:
            return self.async_show_form(step_id="interaction_log", data_schema=schema)

        self.new_data[CONF_INTERACTION_LOG_ENABLED] = user_input[
            CONF_INTERACTION_LOG_ENABLED
        ]

        if self.config_entry:
            return await self.update_or_create()

        if self._auth_type == "api":
            return await self.async_step_select_device()
        return await self.async_step_manual_device_input()

    async def async_step_api(self, user_input: dict[str, Any] | None = None):
        api_keys_auth_schema = vol.Schema(
            {
                vol.Required(CONF_API_HOST): selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=["api-e.ecoflow.com", "api-a.ecoflow.com"],
                        mode=selector.SelectSelectorMode.DROPDOWN,
                    ),
                ),
                vol.Required(
                    CONF_ACCESS_KEY, default=self.new_data.get(CONF_ACCESS_KEY, "")
                ): str,
                vol.Required(
                    CONF_SECRET_KEY, default=self.new_data.get(CONF_SECRET_KEY, "")
                ): str,
            }
        )

        if not user_input:
            return self.async_show_form(step_id="api", data_schema=api_keys_auth_schema)

        self.new_data[CONF_API_HOST] = user_input.get(CONF_API_HOST)
        self.new_data[CONF_ACCESS_KEY] = user_input.get(CONF_ACCESS_KEY)
        self.new_data[CONF_SECRET_KEY] = user_input.get(CONF_SECRET_KEY)

        from .api.public_api import EcoflowPublicApiClient

        self.auth = EcoflowPublicApiClient(
            self.new_data[CONF_API_HOST],
            self.new_data[CONF_ACCESS_KEY],
            self.new_data[CONF_SECRET_KEY],
            self.new_data[CONF_GROUP],
        )
        self._auth_type = "api"

        errors: Dict[str, str] = {}
        try:
            await self.auth.login()
        except EcoflowException as e:  # pylint: disable=broad-except
            errors["base"] = str(e)
        except Exception:  # pylint: disable=broad-except
            _LOGGER.exception("Unexpected exception in login action")
            return self.async_abort(reason="unknown")

        if errors:
            return self.async_show_form(
                step_id="api", data_schema=api_keys_auth_schema, errors=errors
            )

        if self.config_entry:  # reconfig flow
            devices = extract_devices(self.config_entry)
            self.set_local_device_list(list(devices.values()))

            return self.async_show_menu(
                step_id="api",
                menu_options=[
                    "api_add_device",
                    "remove_device",
                    "mqtt",
                    "interaction_log",
                    "finish",
                ],
            )
        else:
            return await self.async_step_mqtt()

    async def async_step_api_add_device(self, user_input: dict[str, Any] | None = None):
        return await self.async_step_select_device()

    async def async_step_finish(self, user_input: dict[str, Any] | None = None):
        return await self.update_or_create()

    async def async_step_remove_device(self, user_input: dict[str, Any] | None = None):
        if len(self.local_devices) == 1:
            return self.async_abort(reason="remove_last_device")

        if not user_input:
            return self.async_show_form(
                step_id="remove_device",
                last_step=True,
                data_schema=vol.Schema(
                    {
                        vol.Required(CONF_SELECT_DEVICE_KEY): vol.In(
                            list(self.local_devices)
                        )
                    }
                ),
            )
        target_device = self.local_devices[user_input[CONF_SELECT_DEVICE_KEY]]
        if target_device.sn in self.new_data[CONF_DEVICE_LIST]:
            self.new_data[CONF_DEVICE_LIST].pop(target_device.sn)

        self.remove_device(target_device.sn)
        return await self.update_or_create()

    async def async_step_select_device(self, user_input: dict[str, Any] | None = None):
        if not user_input:
            try:
                devices = await self.auth.fetch_all_available_devices()
                self.set_device_list(devices)
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception in fetch device action")
                return self.async_abort(reason="unknown")

            target_devices = [
                k for k, v in self.cloud_devices.items() if k not in self.local_devices
            ]
            if len(target_devices) < 1:
                return self.async_abort(reason="no_device_to_add")

            return self.async_show_form(
                step_id="select_device",
                data_schema=vol.Schema(
                    {vol.Required(CONF_SELECT_DEVICE_KEY): vol.In(list(target_devices))}
                ),
            )

        self.cloud_device = self.cloud_devices[user_input[CONF_SELECT_DEVICE_KEY]]

        return await self.async_step_confirm_cloud_device()

    async def async_step_confirm_cloud_device(
        self, user_input: dict[str, Any] | None = None
    ):
        from .devices.registry import device_by_product

        if not user_input:
            device_list = list(device_by_product.keys())
            return self.async_show_form(
                step_id="confirm_cloud_device",
                data_schema=vol.Schema(
                    {
                        vol.Required(
                            CONF_DEVICE_TYPE, default=self.cloud_device.device_type
                        ): selector.SelectSelector(
                            selector.SelectSelectorConfig(
                                options=device_list,
                                mode=selector.SelectSelectorMode.DROPDOWN,
                            ),
                        ),
                        vol.Required(
                            CONF_DEVICE_NAME, default=self.cloud_device.name
                        ): str,
                        vol.Required(CONF_DEVICE_ID, default=self.cloud_device.sn): str,
                    }
                ),
            )

        device = device_by_product[user_input[CONF_DEVICE_TYPE]]

        sn = user_input[CONF_DEVICE_ID]

        if CONF_DEVICE_LIST not in self.new_data:
            self.new_data[CONF_DEVICE_LIST] = {}
            self.new_options[CONF_DEVICE_LIST] = {}

        self.new_data[CONF_DEVICE_LIST][sn] = {
            CONF_DEVICE_NAME: user_input[CONF_DEVICE_NAME],
            CONF_DEVICE_TYPE: user_input[CONF_DEVICE_TYPE],
        }
        self.new_options[CONF_DEVICE_LIST][sn] = {
            OPTS_REFRESH_PERIOD_SEC: DEFAULT_REFRESH_PERIOD_SEC,
            OPTS_POWER_STEP: device.default_charging_power_step(),
            OPTS_DIAGNOSTIC_MODE: (
                "Diagnostic".lower() == user_input[CONF_DEVICE_TYPE].lower()
            ),
        }

        return await self.update_or_create()

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: ConfigEntry) -> EcoflowOptionsFlow:
        return EcoflowOptionsFlow(config_entry)


class EcoflowOptionsFlow(OptionsFlowWithConfigEntry):
    def __init__(self, config_entry: ConfigEntry) -> None:
        super().__init__(config_entry)
        self.devices: dict[str, DeviceData] = extract_devices(self.config_entry)
        self.device_selector = {}
        for _, device in self.devices.items():
            self.device_selector[f"{device.name} ({device.sn})"] = device

        self.selected_device = None

    async def async_step_init(self, user_input: dict[str, Any] | None = None):
        if user_input is None:
            return self.async_show_form(
                step_id="init",
                data_schema=vol.Schema(
                    {
                        vol.Required(CONF_SELECT_DEVICE_KEY): vol.In(
                            list(self.device_selector.keys())
                        )
                    }
                ),
            )

        self.selected_device = self.device_selector[user_input[CONF_SELECT_DEVICE_KEY]]
        return await self.async_step_options()

    async def async_step_options(self, user_input: dict[str, Any] | None = None):
        if user_input is None:
            device_options: DeviceOptions = self.devices[
                self.selected_device.sn
            ].options

            return self.async_show_form(
                step_id="options",
                last_step=True,
                data_schema=vol.Schema(
                    {
                        vol.Required(
                            OPTS_POWER_STEP, default=device_options.power_step
                        ): int,
                        vol.Required(
                            OPTS_REFRESH_PERIOD_SEC,
                            default=device_options.refresh_period,
                        ): int,
                        vol.Required(
                            OPTS_DIAGNOSTIC_MODE, default=device_options.diagnostic_mode
                        ): bool,
                    }
                ),
            )

        new_options = {**self.config_entry.options}
        new_options[CONF_DEVICE_LIST][self.selected_device.sn] = {
            OPTS_POWER_STEP: user_input[OPTS_POWER_STEP],
            OPTS_REFRESH_PERIOD_SEC: user_input[OPTS_REFRESH_PERIOD_SEC],
            OPTS_DIAGNOSTIC_MODE: user_input[OPTS_DIAGNOSTIC_MODE],
        }

        return self.async_create_entry(title="", data=new_options)
