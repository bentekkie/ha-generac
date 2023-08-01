"""Image platform for generac."""
from typing import Type

from homeassistant.components.weather import WeatherEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DEFAULT_NAME
from .const import DOMAIN
from .coordinator import GeneracDataUpdateCoordinator
from .entity import GeneracEntity
from .models import Item


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
):
    """Setup binary_sensor platform."""
    coordinator: GeneracDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    data = coordinator.data
    if isinstance(data, dict):
        async_add_entities(
            sensor(coordinator, entry, generator_id, item)
            for generator_id, item in data.items()
            for sensor in sensors(item)
        )


def sensors(item: Item) -> list[Type[GeneracEntity]]:
    return [HeroImageSensor]


class HeroImageSensor(GeneracEntity, WeatherEntity):
    """generac Image class."""

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{DEFAULT_NAME}_{self.generator_id}_hero_image"

    @property
    def image_url(self):
        return self.aparatus_detail.heroImageUrl
