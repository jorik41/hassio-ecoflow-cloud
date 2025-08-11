import logging
import requests
import io
import re
from datetime import timedelta

from pdfminer.high_level import extract_text
from homeassistant.components.sensor import SensorEntity
from homeassistant.const import CONF_NAME, CONF_URL
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
    UpdateFailed,
)

_LOGGER = logging.getLogger(__name__)
DOMAIN = "engie_gas"


def parse_pdf(url):
    """Download de PDF, extraheer de tekst en parse de gewenste waarden.
    
    Geeft een dictionary terug met de volgende keys:
      - maandelijkse_prijs
      - fluvius_zenne_dijle_afname
      - fluvius_zenne_dijle_vergoeding
      - energiebijdrage
      - verbruik_0_12000
      - totaal  (berekend als maandelijkse_prijs + energiebijdrage + verbruik_0_12000)
    """
    result = {}
    try:
        response = requests.get(url)
        response.raise_for_status()
        pdf_bytes = response.content

        with io.BytesIO(pdf_bytes) as pdf_file:
            text = extract_text(pdf_file)

        if not text:
            _LOGGER.error("Geen tekst gevonden in de PDF.")
            return None

        _LOGGER.debug("Extracted text: %s", text)

        # Maandelijkse prijs: zoekt naar "Maandelijkse prijzen" gevolgd door een regel met getal
        m_price = re.search(r'Maandelijkse prijzen\s*\n\s*([\d,]+)', text)
        if m_price:
            try:
                result["maandelijkse_prijs"] = float(m_price.group(1).replace(',', '.'))
            except ValueError:
                _LOGGER.error("Kon de maandelijkse prijs niet omzetten: %s", m_price.group(1))
        else:
            _LOGGER.error("Geen maandelijkse prijs gevonden.")

        # FLUVIUS ZENNE-DIJLE: verwacht een regel als:
        # FLUVIUS ZENNE-DIJLE 16,66 2,391 88,46 0,955 598,01 0,616 18,56 0,165
        flz_match = re.search(
            r'FLUVIUS ZENNE-DIJLE\s+[\d,]+\s+[\d,]+\s+[\d,]+\s+([\d,]+)\s+[\d,]+\s+[\d,]+\s+[\d,]+\s+([\d,]+)',
            text)
        if flz_match:
            try:
                result["fluvius_zenne_dijle_afname"] = float(flz_match.group(1).replace(',', '.'))
                result["fluvius_zenne_dijle_vergoeding"] = float(flz_match.group(2).replace(',', '.'))
            except ValueError:
                _LOGGER.error("Kon de FLUVIUS ZENNE-DIJLE waarden niet omzetten: %s, %s",
                              flz_match.group(1), flz_match.group(2))
        else:
            _LOGGER.error("Geen waarden voor FLUVIUS ZENNE-DIJLE gevonden.")

        # Verwerk het toeslagen-blok: we zoeken naar het gedeelte na "Toeslagen (€cent/kWh)"
        toeslagen_match = re.search(r'Toeslagen\s*\(.*?\)(.*)', text, re.DOTALL)
        if toeslagen_match:
            block = toeslagen_match.group(1)
            lines = block.splitlines()
            # Verzamel alleen lijnen die volledig bestaan uit cijfers en komma's
            numbers_in_block = [line.strip() for line in lines if re.fullmatch(r'[\d,]+', line.strip())]
            _LOGGER.debug("Getallen in toeslagen-blok: %s", numbers_in_block)
            if len(numbers_in_block) >= 2:
                try:
                    result["energiebijdrage"] = float(numbers_in_block[0].replace(',', '.'))
                    result["verbruik_0_12000"] = float(numbers_in_block[1].replace(',', '.'))
                except ValueError:
                    _LOGGER.error("Fout bij het omzetten van getallen in toeslagen-blok: %s", numbers_in_block)
            else:
                _LOGGER.error("Niet genoeg getallen gevonden in toeslagen-blok voor Energiebijdrage en Verbruik tussen 0 & 12.000 kWh.")
        else:
            _LOGGER.error("Toeslagen-blok niet gevonden.")

        # Bereken totaal als alle drie waarden beschikbaar zijn
        if ("maandelijkse_prijs" in result and 
            "energiebijdrage" in result and 
            "verbruik_0_12000" in result):
            result["totaal"] = (result["maandelijkse_prijs"] +
                                result["energiebijdrage"] +
                                result["verbruik_0_12000"])
        else:
            _LOGGER.error("Niet alle waarden beschikbaar voor totaal berekening.")

        return result

    except Exception as e:
        _LOGGER.error("Fout bij ophalen of parsen van de PDF: %s", e)
        return None


class EngieGasCoordinator(DataUpdateCoordinator):
    """Haal en cache de Engie gasprijzen."""

    def __init__(self, hass, url):
        super().__init__(
            hass,
            _LOGGER,
            name="Engie gas data",
            update_interval=timedelta(days=1),
        )
        self.url = url

    async def _async_update_data(self):  # noqa: D401
        """Fetch data from the Engie PDF."""
        data = await self.hass.async_add_executor_job(parse_pdf, self.url)
        if data is None:
            raise UpdateFailed("Geen gegevens opgehaald")
        return data


class EngieGasSensor(CoordinatorEntity, SensorEntity):
    """Sensor voor een specifiek getal uit de Engie PDF."""

    def __init__(self, coordinator, name, unique_id, sensor_type):
        super().__init__(coordinator)
        self._sensor_type = sensor_type
        self._attr_unique_id = f"{unique_id}_{sensor_type}"
        self._attr_name = f"{name} {self._sensor_friendly_name(sensor_type)}"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, unique_id)},
            "name": name,
            "manufacturer": "Engie",
            "model": "Gas Price PDF Sensor",
        }
        self._attr_state_class = "measurement"
        self._attr_native_unit_of_measurement = "€cent/kWh"

    @staticmethod
    def _sensor_friendly_name(sensor_type):
        names = {
            "maandelijkse_prijs": "Maandelijkse Prijs",
            "fluvius_zenne_dijle_afname": "FL Zenne-Dijle Afname",
            "fluvius_zenne_dijle_vergoeding": "FL Zenne-Dijle Vergoeding",
            "energiebijdrage": "Energiebijdrage",
            "verbruik_0_12000": "Verbruik 0-12kWh",
            "totaal": "Totaal",
        }
        return names.get(sensor_type, sensor_type)

    @property
    def native_value(self):  # noqa: D401
        """Return the current value for this sensor type."""
        return self.coordinator.data.get(self._sensor_type)


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Stel de sensoren in vanuit een config entry."""
    name = config_entry.data.get(CONF_NAME, "Engie Prijzen")
    url = config_entry.data.get(CONF_URL)
    unique_id = config_entry.entry_id

    coordinator = EngieGasCoordinator(hass, url)
    await coordinator.async_config_entry_first_refresh()

    entities = [
        EngieGasSensor(coordinator, name, unique_id, "maandelijkse_prijs"),
        EngieGasSensor(coordinator, name, unique_id, "fluvius_zenne_dijle_afname"),
        EngieGasSensor(coordinator, name, unique_id, "fluvius_zenne_dijle_vergoeding"),
        EngieGasSensor(coordinator, name, unique_id, "energiebijdrage"),
        EngieGasSensor(coordinator, name, unique_id, "verbruik_0_12000"),
        EngieGasSensor(coordinator, name, unique_id, "totaal"),
    ]
    async_add_entities(entities)
