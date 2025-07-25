from __future__ import annotations

import json
import logging
from homeassistant.core import HomeAssistant
import asyncio

_LOGGER = logging.getLogger(__name__)

class EnergyStore:
    def __init__(self, hass: HomeAssistant) -> None:
        self._hass = hass
        self._path = hass.config.path("ecoflow_energy.json")
        self._data: dict[str, dict[str, float | str]] = {}
        self._save_lock = asyncio.Lock()
        self._save_task: asyncio.Task | None = None
        self._pending_save = False

    @classmethod
    async def async_create(cls, hass: HomeAssistant) -> "EnergyStore":
        """Create a store and load data asynchronously."""
        store = cls(hass)
        await store.async_load()
        return store

    def _load_sync(self) -> dict[str, dict[str, float | str]]:
        try:
            with open(self._path, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
        except Exception as err:
            _LOGGER.error("Failed to load energy store: %s", err)
            return {}

    async def async_load(self) -> None:
        """Load data from disk without blocking the event loop."""
        self._data = await self._hass.async_add_executor_job(self._load_sync)

    def _save_sync(self) -> None:
        try:
            with open(self._path, "w", encoding="utf-8") as f:
                json.dump(self._data, f)
        except Exception as err:
            _LOGGER.error("Failed to save energy store: %s", err)

    async def _save_worker(self) -> None:
        async with self._save_lock:
            await self._hass.async_add_executor_job(self._save_sync)
            while self._pending_save:
                self._pending_save = False
                await self._hass.async_add_executor_job(self._save_sync)
        self._save_task = None

    def _ensure_save(self) -> None:
        if self._save_task is None or self._save_task.done():
            self._save_task = self._hass.async_create_task(self._save_worker())
        else:
            self._pending_save = True

    async def async_save(self) -> None:
        """Public method to force an immediate save."""
        self._ensure_save()
        if self._save_task is not None:
            await self._save_task

    def get(self, key: str, default: dict[str, float | str] | None = None):
        return self._data.get(key, default)

    def set(self, key: str, value: dict[str, float | str]) -> None:
        self._data[key] = value
        self._ensure_save()

    async def async_close(self) -> None:
        if self._save_task:
            self._save_task.cancel()
            try:
                await self._save_task
            except asyncio.CancelledError:
                pass
