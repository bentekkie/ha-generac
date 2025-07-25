"""Adds config flow for generac."""
import logging

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers.aiohttp_client import async_create_clientsession

from .api import GeneracApiClient
from .api import InvalidCredentialsException
from .const import CONF_PASSWORD
from .const import CONF_USERNAME
from .const import CONF_COOKIES
from .const import CONF_AUTH_TOKEN
from .const import CONF_AUTH_METHOD
from .const import AUTH_METHOD_USERNAME_PASSWORD
from .const import AUTH_METHOD_COOKIES
from .const import AUTH_METHOD_TOKEN
from .const import DOMAIN
from .const import PLATFORMS


_LOGGER: logging.Logger = logging.getLogger(__package__)


class GeneracFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for generac."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    def __init__(self):
        """Initialize."""
        self._errors = {}
        self._auth_method = AUTH_METHOD_USERNAME_PASSWORD

    async def async_step_user(self, user_input=None):
        """Handle initial auth method selection."""
        self._errors = {}

        if user_input is not None:
            self._auth_method = user_input[CONF_AUTH_METHOD]
            if self._auth_method == AUTH_METHOD_USERNAME_PASSWORD:
                return await self.async_step_username_password()
            elif self._auth_method == AUTH_METHOD_COOKIES:
                return await self.async_step_cookies()
            elif self._auth_method == AUTH_METHOD_TOKEN:
                return await self.async_step_token()

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_AUTH_METHOD, default=AUTH_METHOD_USERNAME_PASSWORD): vol.In({
                    AUTH_METHOD_USERNAME_PASSWORD: "Username & Password",
                    AUTH_METHOD_COOKIES: "Browser Cookies",
                    AUTH_METHOD_TOKEN: "JWT Token"
                })
            }),
            errors=self._errors,
        )

    async def async_step_username_password(self, user_input=None):
        """Handle username/password authentication."""
        if user_input is not None:
            error = await self._test_credentials(
                username=user_input[CONF_USERNAME], 
                password=user_input[CONF_PASSWORD]
            )
            if error is None:
                user_input[CONF_AUTH_METHOD] = AUTH_METHOD_USERNAME_PASSWORD
                return self.async_create_entry(
                    title=user_input[CONF_USERNAME], data=user_input
                )
            else:
                self._errors["base"] = error

        return self.async_show_form(
            step_id="username_password",
            data_schema=vol.Schema({
                vol.Required(CONF_USERNAME): str, 
                vol.Required(CONF_PASSWORD): str
            }),
            errors=self._errors,
        )

    async def async_step_cookies(self, user_input=None):
        """Handle browser cookies authentication."""
        if user_input is not None:
            error = await self._test_credentials(cookies=user_input[CONF_COOKIES])
            if error is None:
                user_input[CONF_AUTH_METHOD] = AUTH_METHOD_COOKIES
                return self.async_create_entry(
                    title="Generac (Cookies)", data=user_input
                )
            else:
                self._errors["base"] = error

        return self.async_show_form(
            step_id="cookies",
            data_schema=vol.Schema({
                vol.Required(CONF_COOKIES): str
            }),
            errors=self._errors,
            description_placeholders={
                "instructions": "Login to Generac web app, open DevTools (F12) → Application/Storage → Cookies, copy all cookies for mobilelinkgen.com domain as: name1=value1; name2=value2"
            }
        )

    async def async_step_token(self, user_input=None):
        """Handle JWT token authentication."""
        if user_input is not None:
            error = await self._test_credentials(auth_token=user_input[CONF_AUTH_TOKEN])
            if error is None:
                user_input[CONF_AUTH_METHOD] = AUTH_METHOD_TOKEN
                return self.async_create_entry(
                    title="Generac (JWT Token)", data=user_input
                )
            else:
                self._errors["base"] = error

        return self.async_show_form(
            step_id="token",
            data_schema=vol.Schema({
                vol.Required(CONF_AUTH_TOKEN): str
            }),
            errors=self._errors,
            description_placeholders={
                "instructions": "Use mobile app proxy capture or extract JWT token from Authorization: Bearer header"
            }
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return GeneracOptionsFlowHandler(config_entry)

    async def _test_credentials(self, username=None, password=None, cookies=None, auth_token=None):
        """Test if credentials are valid."""
        try:
            session = async_create_clientsession(self.hass)
            client = GeneracApiClient(
                username=username, 
                password=password, 
                session=session,
                cookies=cookies,
                auth_token=auth_token
            )
            await client.async_get_data()
            return None
        except InvalidCredentialsException as e:  # pylint: disable=broad-except
            _LOGGER.debug("ERROR in testing credentials: %s", e)
            return "auth"
        except Exception as e:  # pylint: disable=broad-except
            _LOGGER.debug("ERROR: %s", e)
            return "internal"


class GeneracOptionsFlowHandler(config_entries.OptionsFlow):
    """Config flow options handler for generac."""

    def __init__(self, config_entry):
        """Initialize HACS options flow."""
        self.config_entry = config_entry
        self.options = dict(config_entry.options)

    async def async_step_init(self, user_input=None):  # pylint: disable=unused-argument
        """Manage the options."""
        return await self.async_step_user()

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        if user_input is not None:
            self.options.update(user_input)
            return await self._update_options()

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(x, default=self.options.get(x, True)): bool
                    for x in sorted(PLATFORMS)
                }
            ),
        )

    async def _update_options(self):
        """Update config entry options."""
        return self.async_create_entry(
            title=self.config_entry.data.get(CONF_USERNAME), data=self.options
        )
