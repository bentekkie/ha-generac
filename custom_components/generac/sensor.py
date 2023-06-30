"""Sensor platform for generac."""
from datetime import datetime
from typing import Type

from homeassistant.components.sensor import SensorDeviceClass
from homeassistant.components.sensor import SensorEntity
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


def sensors() -> list[Type[GeneracEntity]]:
    return [
        StatusSensor,
        RunTimeSensor,
        ProtectionTimeSensor,
        ActivationDateSensor,
        LastSeenSensor,
        ConnectionTimeSensor,
        BatteryVoltageSensor,
    ]


class StatusSensor(GeneracEntity, SensorEntity):
    """generac Sensor class."""

    options = [
        "Ready",
        "Running",
        "Exercising",
        "Warning",
        "Stopped",
        "Communication Issue",
        "Unknown",
    ]
    icon = "mdi:power"
    device_class = SensorDeviceClass.ENUM

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{DEFAULT_NAME}_{self.generator_id}_status"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        index = self.aparatus_detail.apparatusStatus - 1
        if index < 0 or index > len(self.options) - 1:
            index = len(self.options) - 1
        return self.options[index]

    @property
    def extra_state_attributes(self):
        return {
            "label": self.aparatus_detail.statusLabel,
            "text": self.aparatus_detail.statusText,
        }


class RunTimeSensor(GeneracEntity, SensorEntity):
    """generac Sensor class."""

    device_class = SensorDeviceClass.DURATION
    native_unit_of_measurement = "h"

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{DEFAULT_NAME}_{self.generator_id}_run_time"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        val = next(
            (prop.value for prop in self.aparatus_detail.properties if prop.type == 70),
            0,
        )
        if isinstance(val, str):
            val = float(val)
        return val


class ProtectionTimeSensor(GeneracEntity, SensorEntity):
    """generac Sensor class."""

    device_class = SensorDeviceClass.DURATION
    native_unit_of_measurement = "h"

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{DEFAULT_NAME}_{self.generator_id}_protection_time"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        val = next(
            (prop.value for prop in self.aparatus_detail.properties if prop.type == 31),
            0,
        )
        if isinstance(val, str):
            val = float(val)
        return val


class ActivationDateSensor(GeneracEntity, SensorEntity):
    """generac Sensor class."""

    device_class = SensorDeviceClass.TIMESTAMP

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{DEFAULT_NAME}_{self.generator_id}_activation_date"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return datetime.strptime(
            self.aparatus_detail.activationDate, "%Y-%m-%dT%H:%M:%S%z"
        )


class LastSeenSensor(GeneracEntity, SensorEntity):
    """generac Sensor class."""

    device_class = SensorDeviceClass.TIMESTAMP

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{DEFAULT_NAME}_{self.generator_id}_last_seen"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return datetime.strptime(
            self.aparatus_detail.lastSeen, "%Y-%m-%dT%H:%M:%S.%f%z"
        )


class ConnectionTimeSensor(GeneracEntity, SensorEntity):
    """generac Sensor class."""

    device_class = SensorDeviceClass.TIMESTAMP

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{DEFAULT_NAME}_{self.generator_id}_connection_time"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return datetime.strptime(
            self.aparatus_detail.connectionTimestamp, "%Y-%m-%dT%H:%M:%S.%f%z"
        )


class BatteryVoltageSensor(GeneracEntity, SensorEntity):
    """generac Sensor class."""

    device_class = SensorDeviceClass.VOLTAGE
    native_unit_of_measurement = "V"

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{DEFAULT_NAME}_{self.generator_id}_battery_voltage"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        val = next(
            (prop.value for prop in self.aparatus_detail.properties if prop.type == 69),
            0,
        )
        if isinstance(val, str):
            val = float(val)
        return val


# class SignalStrengthSensor(GeneracEntity, SensorEntity):
#     """generac Sensor class."""
#     device_class = SensorDeviceClass.SIGNAL_STRENGTH
#     native_unit_of_measurement = "db"

#     @property
#     def name(self):
#         """Return the name of the sensor."""
#         return f"{DEFAULT_NAME}_{self.generator_id}_signal_strength"

#     @property
#     def native_value(self):
#         """Return the state of the sensor."""
#         val = next((prop.value for prop in self.aparatus.properties if prop.type == 69), 0)
#         if isinstance(val, int):
#             return 0
#         if val.signalStrength is None:
#             return 0
