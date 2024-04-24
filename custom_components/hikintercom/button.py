import logging

from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from . import HikCoordinator
from .const import DOMAIN
from .core.hikvision import Intercom

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
        hass: HomeAssistant,
        config_entry: ConfigEntry,
        async_add_entities: AddEntitiesCallback
) -> None:
    entry_id = config_entry.entry_id
    coordinator: HikCoordinator = hass.data[DOMAIN][entry_id]
    intercom = coordinator.intercom
    buttons = []
    for number in range(1, intercom.quantity + 1):
        unique_id = f'{intercom.info.id}-{number}'
        buttons.append(OpenButton(intercom, number, unique_id))

    if buttons:
        async_add_entities(buttons)
        _LOGGER.debug(f'Добавлены кнопки: {buttons}')


class OpenButton(ButtonEntity):

    _attr_icon = 'mdi:doorbell-video'

    def __init__(
            self,  intercom: Intercom, number: int, unique_id: str
    ) -> None:
        self._intercom = intercom
        self._number = number
        self._unique_id = unique_id

    @property
    def name(self) -> str:
        return f'Открыть дверь №{self._number}'

    @property
    def unique_id(self) -> str:
        return self._unique_id

    @property
    def device_info(self):
        return {"identifiers": {(DOMAIN, self._intercom.info.id)}}

    def __repr__(self) -> str:
        if not self.hass:
            return f"<Button entity {self.name}>"
        return super().__repr__()

    async def async_press(self) -> None:
        """Handle the button press."""
        await self._intercom.open_door(self._number)
