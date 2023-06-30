import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.helpers.update_coordinator import UpdateFailed

from .api import GeneracApiClient
from .const import DOMAIN
from .models import Item

SCAN_INTERVAL = timedelta(seconds=30)

_LOGGER: logging.Logger = logging.getLogger(__package__)


class GeneracDataUpdateCoordinator(DataUpdateCoordinator[dict[str, Item]]):
    """Class to manage fetching data from the API."""

    def __init__(
        self,
        hass: HomeAssistant,
        client: GeneracApiClient,
        config_entry: ConfigEntry
    ) -> None:
        """Initialize."""
        self.hass = hass
        self.api = client
        self._config_entry = config_entry
        self.platforms = []
        self.is_online = False

        super().__init__(hass, _LOGGER, name=DOMAIN, update_interval=SCAN_INTERVAL)

    async def _async_update_data(self):
        """Update data via library."""
        try:
            _LOGGER.debug("Refreshing data for generac")
            items = await self.api.async_get_data()
            self.is_online = items is not None
            return items
        except Exception as exception:
            raise UpdateFailed() from exception
