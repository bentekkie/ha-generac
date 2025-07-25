"""
Custom integration to integrate generac with Home Assistant.

For more details about this integration, please refer to
https://github.com/bentekkie/generac
"""
import asyncio
import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import GeneracApiClient
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
from .const import STARTUP_MESSAGE
from .coordinator import GeneracDataUpdateCoordinator

SCAN_INTERVAL = timedelta(seconds=30)

_LOGGER: logging.Logger = logging.getLogger(__package__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up this integration using UI."""
    if hass.data.get(DOMAIN) is None:
        hass.data.setdefault(DOMAIN, {})
        _LOGGER.info(STARTUP_MESSAGE)

    auth_method = entry.data.get(CONF_AUTH_METHOD, AUTH_METHOD_USERNAME_PASSWORD)
    session = async_get_clientsession(hass)
    
    # Create client based on authentication method
    if auth_method == AUTH_METHOD_TOKEN:
        auth_token = entry.data.get(CONF_AUTH_TOKEN)
        client = GeneracApiClient(session=session, auth_token=auth_token)
    elif auth_method == AUTH_METHOD_COOKIES:
        cookies = entry.data.get(CONF_COOKIES)
        client = GeneracApiClient(session=session, cookies=cookies)
    else:  # username_password
        username = entry.data.get(CONF_USERNAME, "")
        password = entry.data.get(CONF_PASSWORD, "")
        client = GeneracApiClient(username=username, password=password, session=session)

    coordinator = GeneracDataUpdateCoordinator(hass, client=client, config_entry=entry)
    await coordinator.async_config_entry_first_refresh()

    if not coordinator.last_update_success:
        raise ConfigEntryNotReady

    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    entry.add_update_listener(async_reload_entry)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Handle removal of an entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    unloaded = all(
        await asyncio.gather(
            *[
                hass.config_entries.async_forward_entry_unload(entry, platform)
                for platform in PLATFORMS
                if platform in coordinator.platforms
            ]
        )
    )
    if unloaded:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unloaded


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
