import logging
import httpx
import xmltodict

from homeassistant.helpers.typing import HomeAssistantType
from homeassistant.helpers.httpx_client import get_async_client

from .model_hikvision import DeviceInfo
from ..const import (
    HTTP_URL, URL_GET_INFO
)

_LOGGER = logging.getLogger(__name__)


class Intercom:
    """Класс видеодомофона"""

    device_info: DeviceInfo

    def __init__(
            self, hass: HomeAssistantType, ip: str, login: str, password: str
    ):
        self.ip = ip
        self.login = login
        self.password = password
        self.session = get_async_client(hass)
        _LOGGER.debug(f'Создан объект Intercom')

    async def update_device_info(self):
        response = await self.session.get(
            url=HTTP_URL + self.ip + URL_GET_INFO,
            auth=httpx.DigestAuth(self.login, self.password)
        )
        self.device_info = DeviceInfo.parse_obj(xmltodict.parse(response.text))
        _LOGGER.debug(self.device_info)
