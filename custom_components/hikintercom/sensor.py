import logging

from homeassistant.components.sensor import SensorEntity, SensorDeviceClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity
)
from . import HikCoordinator
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
        hass: HomeAssistant,
        config_entry: ConfigEntry,
        async_add_entities: AddEntitiesCallback
) -> None:
    entry_id = config_entry.entry_id
    coordinator: HikCoordinator = hass.data[DOMAIN][entry_id]
    sensors = [StatusIntercom(coordinator)]
    async_add_entities(sensors)
    _LOGGER.debug(f'Добавлены сенсоры: {sensors}')


class StatusIntercom(CoordinatorEntity, SensorEntity):

    _attr_icon = 'mdi:bell'
    options = []

    def __init__(self, coordinator: HikCoordinator,) -> None:
        super().__init__(coordinator)
        self._unique_id = f'{coordinator.intercom.info.id}-status'

    def convert_status(self, status: str) -> str:
        match status:
            case 'idle':
                self._attr_icon = 'mdi:bell'
                return 'Закрыто'
            case 'ring':
                self._attr_icon = 'mdi:bell-ring'
                return 'Вызов'
            case 'onCall':
                self._attr_icon = 'mdi:bell-remove-outline'
                return 'Занят'
            case _:
                self._attr_icon = 'mdi:bell-remove-outline'
                return 'Неизвестно'

    @property
    def name(self) -> str:
        return 'Статус домофона'

    @property
    def native_value(self) -> str:
        """Возвращает состояние сенсора"""
        return self.convert_status(self.coordinator.intercom.status)

    @property
    def device_class(self) -> str | None:
        return SensorDeviceClass.ENUM

    @property
    def unique_id(self) -> str:
        return f'{self.coordinator.intercom.info.id}-status'

    def __repr__(self) -> str:
        if not self.hass:
            return f"<Sensor entity {self.name}>"
        return super().__repr__()

    @property
    def device_info(self):
        return {"identifiers": {(DOMAIN, self.coordinator.intercom.info.id)}}
