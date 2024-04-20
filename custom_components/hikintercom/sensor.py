import logging

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
)
from .const import DOMAIN, MANUFACTURER

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
        hass: HomeAssistant,
        config_entry: ConfigEntry,
        async_add_entities: AddEntitiesCallback
) -> None:
    entry_id = config_entry.entry_id

    hik = hass.data[DOMAIN][entry_id]


class StateSensor(CoordinatorEntity, SensorEntity):

    def __init__(
            self, unique_id: str
    ) -> None:
        self._unique_id = unique_id

    @property
    def name(self) -> str:
        return ''

    @property
    def native_value(self) -> float | str:
        """Возвращает состояние сенсора"""
        return ''

    @property
    def unique_id(self) -> str:
        return self._unique_id

    def __repr__(self) -> str:
        if not self.hass:
            return f"<Sensor entity {self.name}>"
        return super().__repr__()

    # @property
    # def device_info(self):
    #     return {
    #         "identifiers": {(DOMAIN, self._sensor.id)},
    #         "name": self._sensor.id,
    #         "sw_version": None,
    #         "model": self._device.model,
    #         "manufacturer": MANUFACTURER,
    #     }

