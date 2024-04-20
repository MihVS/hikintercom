import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator, UpdateFailed
)
from .const import (
    DOMAIN, TIME_UPDATE, MANUFACTURER, TIME_OUT_UPDATE_DATA
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
        hass: HomeAssistant, config_entry: ConfigEntry) -> bool:

    return True


