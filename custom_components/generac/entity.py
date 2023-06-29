"""GeneracEntity class"""
from homeassistant.core import callback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import ATTRIBUTION
from .const import DOMAIN
from .models import Apparatus
from .models import ApparatusDetail


class GeneracEntity(CoordinatorEntity):

    def __init__(self, coordinator, config_entry, generator_id, item):
        super().__init__(coordinator)
        self.config_entry = config_entry
        self.generator_id = generator_id
        self.item = item

    @property
    def unique_id(self):
        """Return a unique ID to use for this entity."""
        return f"{self.config_entry.entry_id}_{self.generator_id}_{self.name}"

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self.generator_id)},
            "name": self.aparatus.name,
            "manufacturer": "Generac",
            "serialNumber": self.aparatus.serialNumber,
            "localizedAddress": self.aparatus.localizedAddress,
            "heroImageUrl": self.aparatus.heroImageUrl,
            "preferredDealerName": self.aparatus.preferredDealerName,
            "preferredDealerPhone": self.aparatus.preferredDealerPhone,
            "preferredDealerEmail": self.aparatus.preferredDealerEmail,
            "modelNumber": self.aparatus.modelNumber,
            "panelId": self.aparatus.panelId,
            "ssid": self.aparatus_detail.deviceSsid,
        }

    @property
    def device_state_attributes(self):
        """Return the state attributes."""
        return {
            "attribution": ATTRIBUTION,
            "id": str(self.generator_id),
            "integration": DOMAIN,
        }

    @property
    def available(self):
        """Return True if entity is available."""
        return self.coordinator.is_online

    async def async_added_to_hass(self) -> None:
        """Connect to dispatcher listening for entity data notifications."""
        self.async_on_remove(
            self.coordinator.async_add_listener(self.async_write_ha_state)
        )

    @property
    def aparatus(self) -> Apparatus:
        return self.item[0]

    @property
    def aparatus_detail(self) -> ApparatusDetail:
        return self.item[1]

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self.item = self.coordinator.data.get(self.generator_id)
        self.async_write_ha_state()
