import logging
from http import HTTPStatus

import aiohttp
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from .const import DOMAIN, HTTP_URL, URL_GET_INFO
from .core.exceptions import InvalidAuth, InvalidIP

_LOGGER = logging.getLogger(__name__)


async def validate_auth(
        hass: HomeAssistant, ip: str, login: str, password: str
) -> None:
    """Валидация авторизации"""

    session = async_get_clientsession(hass)
    response = await session.get(
        url=HTTP_URL + ip + URL_GET_INFO,
        auth=aiohttp.BasicAuth(login, password)
    )
    text = await response.text()
    _LOGGER.debug(text)
    status_code = response.status
    _LOGGER.info(status_code)
    if status_code == HTTPStatus.UNAUTHORIZED:
        error = "Неверный логин или пароль."
        hass.data['error'] = error
        raise InvalidAuth(error)
    elif status_code == HTTPStatus.NOT_FOUND:
        error = "Неверный ip адрес"
        hass.data['error'] = error
        raise InvalidIP(error)


class HikConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1
    data: dict = None

    async def async_step_user(self, user_input=None):
        errors: dict[str, str] = {}
        if user_input is not None:
            try:
                await validate_auth(
                    self.hass,
                    user_input['ip'],
                    user_input['login'],
                    user_input['password']
                )
                if not errors:
                    self.data = user_input
            except InvalidAuth:
                _LOGGER.error("Не правильный логин или пароль")
                errors['base'] = 'invalid_auth'
            except InvalidIP:
                _LOGGER.error("Не правильный IP адрес")
                errors['base'] = 'invalid_ip'
            except Exception as e:
                _LOGGER.error(f'Что-то пошло не так, неизвестная ошибка. {e}')
                errors["base"] = "unknown"
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(schema="ip"): str,
                    vol.Required(schema="login"): str,
                    vol.Required(schema="password"): str
                }
            ),
            errors=errors
        )
