import logging

from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from .const import DOMAIN, MANUFACTURER

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
        hass: HomeAssistant,
        config_entry: ConfigEntry,
        async_add_entities: AddEntitiesCallback
) -> None:
    entry_id = config_entry.entry_id

    hik = hass.data[DOMAIN][entry_id]


class OpenButton(ButtonEntity):

    def __init__(
            self,  unique_id: str
    ) -> None:
        self._unique_id = unique_id

    @property
    def name(self) -> str:
        return ''

    @property
    def unique_id(self) -> str:
        return self._unique_id

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, '')},
            "name": '',
            "model": '',
            "manufacturer": MANUFACTURER
        }

    def __repr__(self) -> str:
        if not self.hass:
            return f"<Button entity {self.name}>"
        return super().__repr__()

    async def async_press(self) -> None:
        """Handle the button press."""
        pass
