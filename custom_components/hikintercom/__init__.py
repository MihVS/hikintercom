import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator, UpdateFailed
)
from .const import (
    DOMAIN, TIME_UPDATE, MANUFACTURER, TIME_OUT_UPDATE_DATA, PLATFORMS
)
from .core.hikvision import Intercom

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
        hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    entry_id = config_entry.entry_id
    ip = config_entry.data.get("ip")
    login = config_entry.data.get("login")
    password = config_entry.data.get("password")
    intercom = Intercom(hass, ip, login, password)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry_id] = intercom
    # await hass.config_entries.async_forward_entry_setups(
    #     config_entry, PLATFORMS
    # )
    return True


