"""Binary sensor platform for generac."""
from homeassistant.components.binary_sensor import BinarySensorDeviceClass
from homeassistant.components.binary_sensor import BinarySensorEntity

from .const import DEFAULT_NAME
from .const import DOMAIN
from .entity import GeneracEntity
from .models import Apparatus
from .models import ApparatusDetail


async def async_setup_entry(hass, entry, async_add_devices):
    """Setup binary_sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    data : dict[str, tuple[Apparatus, ApparatusDetail]] = coordinator.data
    async_add_devices(
        sensor
        for generator_id, item in data.items()
        for sensor in create_sensors(coordinator, entry, generator_id, item)
    )


def create_sensors(coordinator, entry, generator_id, item):
    return [
        GeneracConnectedSensor(coordinator, entry, generator_id, item),
        GeneracConnectingSensor(coordinator, entry, generator_id, item),
        GeneracMaintenanceAlertSensor(coordinator, entry, generator_id, item),
        GeneracWarningSensor(coordinator, entry, generator_id, item),
    ]


class GeneracConnectedSensor(GeneracEntity, BinarySensorEntity):
    """generac binary_sensor class."""

    @property
    def name(self):
        """Return the name of the binary_sensor."""
        return f"{DEFAULT_NAME}_{self.generator_id}_is_connected"

    @property
    def device_class(self):
        """Return the class of this binary_sensor."""
        return BinarySensorDeviceClass.CONNECTIVITY

    @property
    def is_on(self):
        """Return true if the binary_sensor is on."""
        return self.aparatus_detail.isConnected


class GeneracConnectingSensor(GeneracEntity, BinarySensorEntity):
    """generac binary_sensor class."""

    @property
    def name(self):
        """Return the name of the binary_sensor."""
        return f"{DEFAULT_NAME}_{self.generator_id}_is_connecting"

    @property
    def device_class(self):
        """Return the class of this binary_sensor."""
        return BinarySensorDeviceClass.CONNECTIVITY

    @property
    def is_on(self):
        """Return true if the binary_sensor is on."""
        return self.aparatus_detail.isConnecting


class GeneracMaintenanceAlertSensor(GeneracEntity, BinarySensorEntity):
    """generac binary_sensor class."""

    @property
    def name(self):
        """Return the name of the binary_sensor."""
        return f"{DEFAULT_NAME}_{self.generator_id}_has_maintenance_alert"

    @property
    def device_class(self):
        """Return the class of this binary_sensor."""
        return BinarySensorDeviceClass.SAFETY

    @property
    def is_on(self):
        """Return true if the binary_sensor is on."""
        return self.aparatus_detail.hasMaintenanceAlert


class GeneracWarningSensor(GeneracEntity, BinarySensorEntity):
    """generac binary_sensor class."""

    @property
    def name(self):
        """Return the name of the binary_sensor."""
        return f"{DEFAULT_NAME}_{self.generator_id}_show_warning"

    @property
    def device_class(self):
        """Return the class of this binary_sensor."""
        return BinarySensorDeviceClass.SAFETY

    @property
    def is_on(self):
        """Return true if the binary_sensor is on."""
        return self.aparatus_detail.showWarning
