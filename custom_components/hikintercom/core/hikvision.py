import logging
from http import HTTPStatus

import httpx
import xmltodict

from homeassistant.helpers.typing import HomeAssistantType
from homeassistant.helpers.httpx_client import get_async_client

from .model_hikvision import BaseDeviseInfo, DeviceInfo, Status, CallStatus
from ..const import (
    HTTP_URL, URL_GET_INFO, URL_GET_STATE, URL_OPEN_DOOR, BOODY_OPEN_DOOR
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
        _LOGGER.debug('Создан объект Intercom')

    async def update_device_info(self):
        response = await self.session.get(
            url=HTTP_URL + self.ip + URL_GET_INFO,
            auth=httpx.DigestAuth(self.login, self.password)
        )
        base_device_info = BaseDeviseInfo.parse_obj(
            xmltodict.parse(response.text)
        )
        self.device_info = base_device_info.device_info
        _LOGGER.debug(f'Обновлена инфо устройства: {self.device_info}')

    async def get_status(self) -> str:
        response = await self.session.get(
            url=HTTP_URL + self.ip + URL_GET_STATE,
            auth=httpx.DigestAuth(self.login, self.password)
        )
        call_status = CallStatus.parse_obj(
            xmltodict.parse(response.text)
        )
        status = call_status.call_status.status
        _LOGGER.debug(f'Состояние вызывной: {status}')
        return status

    async def open_door(self, number):
        response = await self.session.put(
            url=HTTP_URL + self.ip + URL_OPEN_DOOR + number,
            auth=httpx.DigestAuth(self.login, self.password),
            content=BOODY_OPEN_DOOR
        )
        code = response.status_code
        if code != HTTPStatus.OK:
            _LOGGER.error(f'Ошибка открытия двери: {code}')
        _LOGGER.debug(f'Дверь №{number} открыта')
