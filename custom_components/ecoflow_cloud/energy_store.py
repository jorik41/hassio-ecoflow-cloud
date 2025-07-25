from __future__ import annotations
import json
import logging
from homeassistant.core import HomeAssistant

_LOGGER = logging.getLogger(__name__)

class EnergyStore:
    def __init__(self, hass: HomeAssistant):
        self._hass = hass
        self._path = hass.config.path("ecoflow_energy.json")
        self._data: dict[str, dict[str, float | str]] = {}
        self._load()

    def _load(self) -> None:
        try:
            with open(self._path, "r", encoding="utf-8") as f:
                self._data = json.load(f)
        except FileNotFoundError:
            self._data = {}
        except Exception as err:
            _LOGGER.error("Failed to load energy store: %s", err)
            self._data = {}

    def save(self) -> None:
        try:
            with open(self._path, "w", encoding="utf-8") as f:
                json.dump(self._data, f)
        except Exception as err:
            _LOGGER.error("Failed to save energy store: %s", err)

    def get(self, key: str, default: dict[str, float | str] | None = None):
        return self._data.get(key, default)

    def set(self, key: str, value: dict[str, float | str]) -> None:
        self._data[key] = value
        self.save()
