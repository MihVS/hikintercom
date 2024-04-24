import logging
from http import HTTPStatus

import httpx
import xmltodict

from homeassistant.core import HomeAssistant
from homeassistant.helpers.httpx_client import get_async_client
from .model_hikvision import BaseDeviseInfo, DeviceInfo, CallStatus
from ..const import (
    HTTP_URL, URL_GET_INFO, URL_GET_STATE, URL_OPEN_DOOR, BOODY_OPEN_DOOR
)

_LOGGER = logging.getLogger(__name__)


class Intercom:
    """Класс видеодомофона"""

    info: DeviceInfo
    status: str | None

    def __init__(
            self,
            hass: HomeAssistant,
            ip: str,
            login: str,
            password: str,
            quantity: int
    ):
        self.ip = ip
        self.login = login
        self.password = password
        self.quantity = quantity
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
        self.info = base_device_info.device_info
        _LOGGER.debug(f'Обновлена инфо устройства: {self.info}')

    async def update_status(self):
        response = await self.session.get(
            url=HTTP_URL + self.ip + URL_GET_STATE,
            auth=httpx.DigestAuth(self.login, self.password)
        )
        call_status = CallStatus.parse_obj(
            response.json()
        )
        status = call_status.call_status.status
        _LOGGER.debug(f'Состояние вызывной: {status}')
        self.status = status

    async def open_door(self, number):
        response = await self.session.put(
            url=HTTP_URL + self.ip + URL_OPEN_DOOR + str(number),
            auth=httpx.DigestAuth(self.login, self.password),
            content=BOODY_OPEN_DOOR
        )
        code = response.status_code
        if code != HTTPStatus.OK:
            _LOGGER.error(f'Ошибка открытия двери: {code}')
        else:
            _LOGGER.debug(f'Дверь №{number} открыта')
