"""Binary sensor platform for generac."""
from typing import Type

from homeassistant.components.binary_sensor import BinarySensorDeviceClass
from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DEFAULT_NAME
from .const import DOMAIN
from .coordinator import GeneracDataUpdateCoordinator
from .entity import GeneracEntity


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
            for sensor in sensors()
        )


def sensors() -> Type[GeneracEntity]:
    return [
        GeneracConnectedSensor,
        GeneracConnectingSensor,
        GeneracMaintenanceAlertSensor,
        GeneracWarningSensor,
        GeneracServiceModeSensor,
        GeneracVppEnrolledSensor,
        GeneracActiveVppEventSensor,
        GeneracDisconnectedNotificationSensor,
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


class GeneracServiceModeSensor(GeneracEntity, BinarySensorEntity):
    """Service Mode binary sensor from v5 API."""

    @property
    def name(self):
        """Return the name of the binary_sensor."""
        return f"{DEFAULT_NAME}_{self.generator_id}_service_mode_enabled"

    @property
    def device_class(self):
        """Return the class of this binary_sensor."""
        return BinarySensorDeviceClass.POWER

    @property
    def is_on(self):
        """Return true if the binary_sensor is on."""
        return self.aparatus_detail.serviceModeEnabled


class GeneracVppEnrolledSensor(GeneracEntity, BinarySensorEntity):
    """VPP Enrolled binary sensor from v5 API."""

    @property
    def name(self):
        """Return the name of the binary_sensor."""
        return f"{DEFAULT_NAME}_{self.generator_id}_vpp_enrolled"

    @property
    def is_on(self):
        """Return true if the binary_sensor is on."""
        return self.aparatus_detail.enrolledInVpp


class GeneracActiveVppEventSensor(GeneracEntity, BinarySensorEntity):
    """Active VPP Event binary sensor from v5 API."""

    @property
    def name(self):
        """Return the name of the binary_sensor."""
        return f"{DEFAULT_NAME}_{self.generator_id}_active_vpp_event"

    @property
    def is_on(self):
        """Return true if the binary_sensor is on."""
        return self.aparatus_detail.hasActiveVppEvent


class GeneracDisconnectedNotificationSensor(GeneracEntity, BinarySensorEntity):
    """Disconnected Notifications binary sensor from v5 API."""

    @property
    def name(self):
        """Return the name of the binary_sensor."""
        return f"{DEFAULT_NAME}_{self.generator_id}_disconnected_notifications"

    @property
    def device_class(self):
        """Return the class of this binary_sensor."""
        return BinarySensorDeviceClass.CONNECTIVITY

    @property
    def is_on(self):
        """Return true if the binary_sensor is on."""
        return self.aparatus_detail.hasDisconnectedNotificationsOn
