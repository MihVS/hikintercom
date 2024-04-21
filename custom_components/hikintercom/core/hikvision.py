import logging

from homeassistant.helpers.typing import HomeAssistantType
from homeassistant.helpers.aiohttp_client import async_get_clientsession


_LOGGER = logging.getLogger(__name__)


class Intercom:
    """Класс видеодомофона"""

    def __init__(
            self, hass: HomeAssistantType, ip: str, login: str, password: str
    ):
        self.ip = ip
        self.login = login
        self.password = password
        self.session = async_get_clientsession(hass)
        _LOGGER.debug(f'Создан объект Intercom')