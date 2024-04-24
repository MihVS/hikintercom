import logging
from datetime import timedelta

import async_timeout

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator, UpdateFailed
)
from .const import (
    DOMAIN, TIME_UPDATE, MANUFACTURER, TIME_OUT_UPDATE_DATA, PLATFORMS,
    CONFIGURATION_URL
)
from .core.hikvision import Intercom

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
        hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    entry_id = config_entry.entry_id
    ip = config_entry.data.get("ip")
    login = config_entry.data.get("login")
    password = config_entry.data.get("password")
    quantity = config_entry.data.get("quantity")
    intercom = Intercom(hass, ip, login, password, quantity)
    await intercom.update_device_info()
    coordinator = HikCoordinator(hass, intercom)
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry_id] = coordinator
    await hass.config_entries.async_forward_entry_setups(
        config_entry, PLATFORMS
    )
    return True


class HikCoordinator(DataUpdateCoordinator):
    """Координатор для общего обновления данных"""

    def __init__(self, hass, intercom):
        super().__init__(
            hass,
            _LOGGER,
            name="hikintercom",
            update_interval=timedelta(seconds=TIME_UPDATE),
        )
        self.intercom: Intercom = intercom

    def devices_info(self):
        device_info = DeviceInfo(**{
            "identifiers": {(DOMAIN, self.intercom.info.id)},
            "name": self.intercom.info.name,
            "sw_version": self.intercom.info.firmware_version,
            "hw_version": self.intercom.info.hardware_version,
            "serial_number": self.intercom.info.serial,
            "configuration_url": CONFIGURATION_URL,
            "model": self.intercom.info.model,
            "manufacturer": MANUFACTURER,
        })
        return device_info

    async def _async_update_data(self):
        """Обновление данных API zont"""
        try:
            async with async_timeout.timeout(TIME_OUT_UPDATE_DATA):
                await self.intercom.update_status()
                return self.intercom
        except Exception as err:
            _LOGGER.error(err)
            raise UpdateFailed(f"Ошибка соединения с ISAPI: {err}")
