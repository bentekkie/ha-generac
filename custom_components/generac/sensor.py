"""Sensor platform for generac."""
from datetime import datetime
from typing import Type

from homeassistant.components.sensor import SensorEntity
from homeassistant.components.sensor.const import SensorDeviceClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfTemperature
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
    """Setup sensor platform."""
    coordinator: GeneracDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    data = coordinator.data
    if isinstance(data, dict):
        async_add_entities(
            sensor(coordinator, entry, generator_id, item)
            for generator_id, item in data.items()
            for sensor in sensors(item)
        )


def sensors(item: Item) -> list[Type[GeneracEntity]]:
    lst = [
        StatusSensor,
        RunTimeSensor,
        ProtectionTimeSensor,
        ActivationDateSensor,
        LastSeenSensor,
        ConnectionTimeSensor,
        BatteryVoltageSensor,
        DeviceTypeSensor,
        DealerEmailSensor,
        DealerNameSensor,
        DealerPhoneSensor,
        AddressSensor,
        StatusTextSensor,
        StatusLabelSensor,
        SerialNumberSensor,
        ModelNumberSensor,
        DeviceSsidSensor,
        PanelIDSensor,
        ExerciseMinutesSensor,
        FuelTypeSensor,
        NetworkTypeSensor,
        CurrentAlarmSensor,
    ]
    if (
        item.apparatusDetail.weather is not None
        and item.apparatusDetail.weather.temperature is not None
        and item.apparatusDetail.weather.temperature.value is not None
    ):
        lst.append(OutdoorTemperatureSensor)
    return lst


def parseDatetime(rawStr: str) -> datetime:
    formats = ["%Y-%m-%dT%H:%M:%S.%f%z", "%Y-%m-%dT%H:%M:%S%z"]
    ves: list[ValueError] = []
    for fmt in formats:
        try:
            return datetime.strptime(rawStr, fmt)
        except ValueError as ve:
            ves.append(ve)
    raise ValueError(f"No known datetime format for raw string {rawStr}")


class StatusSensor(GeneracEntity, SensorEntity):
    """generac Sensor class."""

    _attr_options = [
        "Ready",
        "Running",
        "Exercising",
        "Warning",
        "Stopped",
        "Communication Issue",
        "Unknown",
    ]
    _attr_icon = "mdi:power"
    _attr_device_class = SensorDeviceClass.ENUM

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{DEFAULT_NAME}_{self.generator_id}_status"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        options = self.options
        if options is None:
            return None
        if self.aparatus_detail.apparatusStatus is None:
            return options[-1]
        index = self.aparatus_detail.apparatusStatus - 1
        if index < 0 or index > len(options) - 1:
            index = len(options) - 1
        return options[index]


class DeviceTypeSensor(GeneracEntity, SensorEntity):
    """generac Sensor class."""

    _attr_options = [
        "Wifi",
        "Ethernet",
        "MobileData",
        "Unknown",
    ]
    _attr_device_class = SensorDeviceClass.ENUM

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{DEFAULT_NAME}_{self.generator_id}_device_type"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        options = self.options
        if options is None:
            return None
        if self.aparatus_detail.deviceType is None:
            return options[-1]
        if self.aparatus_detail.deviceType == "wifi":
            return options[0]
        if self.aparatus_detail.deviceType == "eth":
            return options[1]
        if self.aparatus_detail.deviceType == "lte":
            return options[2]
        if self.aparatus_detail.deviceType == "cdma":
            return options[2]
        return options[-1]


class RunTimeSensor(GeneracEntity, SensorEntity):
    """generac Sensor class."""

    _attr_device_class = SensorDeviceClass.DURATION
    _attr_native_unit_of_measurement = "h"

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{DEFAULT_NAME}_{self.generator_id}_run_time"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        if self.aparatus_detail.properties is None:
            return 0
        # v5 API uses type 71 for Engine Hours, v2 API used type 70
        val = next(
            (prop.value for prop in self.aparatus_detail.properties if prop.type == 71),
            None,
        )
        if val is None:
            # Fallback to v2 API type
            val = next(
                (prop.value for prop in self.aparatus_detail.properties if prop.type == 70),
                0,
            )
        if isinstance(val, str):
            val = float(val)
        return val


class ProtectionTimeSensor(GeneracEntity, SensorEntity):
    """generac Sensor class."""

    _attr_device_class = SensorDeviceClass.DURATION
    _attr_native_unit_of_measurement = "h"

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{DEFAULT_NAME}_{self.generator_id}_protection_time"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        if self.aparatus_detail.properties is None:
            return 0
        # v5 API uses type 32 for Hours of Protection, v2 API used type 31
        val = next(
            (prop.value for prop in self.aparatus_detail.properties if prop.type == 32),
            None,
        )
        if val is None:
            # Fallback to v2 API type
            val = next(
                (prop.value for prop in self.aparatus_detail.properties if prop.type == 31),
                0,
            )
        if isinstance(val, str):
            val = float(val)
        return val


class ActivationDateSensor(GeneracEntity, SensorEntity):
    """generac Sensor class."""

    _attr_device_class = SensorDeviceClass.TIMESTAMP

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{DEFAULT_NAME}_{self.generator_id}_activation_date"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        if self.aparatus_detail.activationDate is None:
            return None
        return parseDatetime(self.aparatus_detail.activationDate)


class LastSeenSensor(GeneracEntity, SensorEntity):
    """generac Sensor class."""

    _attr_device_class = SensorDeviceClass.TIMESTAMP

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{DEFAULT_NAME}_{self.generator_id}_last_seen"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        if self.aparatus_detail.lastSeen is None:
            return None
        return parseDatetime(self.aparatus_detail.lastSeen)


class ConnectionTimeSensor(GeneracEntity, SensorEntity):
    """generac Sensor class."""

    _attr_device_class = SensorDeviceClass.TIMESTAMP

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{DEFAULT_NAME}_{self.generator_id}_connection_time"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        if self.aparatus_detail.connectionTimestamp is None:
            return None
        return parseDatetime(self.aparatus_detail.connectionTimestamp)


class BatteryVoltageSensor(GeneracEntity, SensorEntity):
    """generac Sensor class."""

    _attr_device_class = SensorDeviceClass.VOLTAGE
    _attr_native_unit_of_measurement = "V"

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{DEFAULT_NAME}_{self.generator_id}_battery_voltage"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        if self.aparatus_detail.properties is None:
            return 0
        # v5 API uses type 70 for Battery Voltage, v2 API used type 69
        val = next(
            (prop.value for prop in self.aparatus_detail.properties if prop.type == 70),
            None,
        )
        if val is None:
            # Fallback to v2 API type
            val = next(
                (prop.value for prop in self.aparatus_detail.properties if prop.type == 69),
                0,
            )
        if isinstance(val, str):
            val = float(val)
        return val


class OutdoorTemperatureSensor(GeneracEntity, SensorEntity):
    """generac Sensor class."""

    _attr_device_class = SensorDeviceClass.TEMPERATURE

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{DEFAULT_NAME}_{self.generator_id}_outdoor_temperature"

    @property
    def native_unit_of_measurement(self):
        if (
            self.aparatus_detail.weather is None
            or self.aparatus_detail.weather.temperature is None
            or self.aparatus_detail.weather.temperature.unit is None
        ):
            return UnitOfTemperature.CELSIUS
        if "f" in self.aparatus_detail.weather.temperature.unit.lower():
            return UnitOfTemperature.FAHRENHEIT
        return UnitOfTemperature.CELSIUS

    @property
    def native_value(self):
        """Return the state of the sensor."""
        if (
            self.aparatus_detail.weather is None
            or self.aparatus_detail.weather.temperature is None
            or self.aparatus_detail.weather.temperature.value is None
        ):
            return 0
        return self.aparatus_detail.weather.temperature.value


class SerialNumberSensor(GeneracEntity, SensorEntity):
    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{DEFAULT_NAME}_{self.generator_id}_serial_number"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self.aparatus.serialNumber


class ModelNumberSensor(GeneracEntity, SensorEntity):
    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{DEFAULT_NAME}_{self.generator_id}_model_number"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self.aparatus.modelNumber


class DeviceSsidSensor(GeneracEntity, SensorEntity):
    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{DEFAULT_NAME}_{self.generator_id}_device_ssid"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self.aparatus_detail.deviceSsid


class StatusLabelSensor(GeneracEntity, SensorEntity):
    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{DEFAULT_NAME}_{self.generator_id}_status_label"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self.aparatus_detail.statusLabel


class StatusTextSensor(GeneracEntity, SensorEntity):
    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{DEFAULT_NAME}_{self.generator_id}_status_text"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self.aparatus_detail.statusText


class AddressSensor(GeneracEntity, SensorEntity):
    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{DEFAULT_NAME}_{self.generator_id}_address"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self.aparatus.localizedAddress


class DealerNameSensor(GeneracEntity, SensorEntity):
    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{DEFAULT_NAME}_{self.generator_id}_dealer_name"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self.aparatus.preferredDealerName


class DealerEmailSensor(GeneracEntity, SensorEntity):
    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{DEFAULT_NAME}_{self.generator_id}_dealer_email"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self.aparatus.preferredDealerEmail


class DealerPhoneSensor(GeneracEntity, SensorEntity):
    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{DEFAULT_NAME}_{self.generator_id}_dealer_phone"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self.aparatus.preferredDealerPhone


class PanelIDSensor(GeneracEntity, SensorEntity):
    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{DEFAULT_NAME}_{self.generator_id}_panel_id"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self.aparatus.panelId


class ExerciseMinutesSensor(GeneracEntity, SensorEntity):
    """Exercise Minutes sensor from v5 API."""

    _attr_device_class = SensorDeviceClass.DURATION
    _attr_native_unit_of_measurement = "min"

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{DEFAULT_NAME}_{self.generator_id}_exercise_minutes"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        if self.aparatus_detail.properties is None:
            return 0
        # v5 API type 95 for Exercise Minutes
        val = next(
            (prop.value for prop in self.aparatus_detail.properties if prop.type == 95),
            0,
        )
        if isinstance(val, str):
            val = float(val)
        return val


class FuelTypeSensor(GeneracEntity, SensorEntity):
    """Fuel Type sensor from v5 API."""

    _attr_options = [
        "Unknown",
        "Natural Gas", 
        "Propane",
    ]
    _attr_device_class = SensorDeviceClass.ENUM

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{DEFAULT_NAME}_{self.generator_id}_fuel_type"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        if self.aparatus_detail.properties is None:
            return self.options[0]
        # v5 API type 88 for Fuel Type
        val = next(
            (prop.value for prop in self.aparatus_detail.properties if prop.type == 88),
            "0",
        )
        if isinstance(val, str):
            fuel_type_int = int(val)
        else:
            fuel_type_int = val or 0
            
        if fuel_type_int == 1:
            return self.options[1]  # Natural Gas
        elif fuel_type_int == 2:
            return self.options[2]  # Propane
        else:
            return self.options[0]  # Unknown


class NetworkTypeSensor(GeneracEntity, SensorEntity):
    """Network Type sensor from v5 API."""

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{DEFAULT_NAME}_{self.generator_id}_network_type"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self.aparatus_detail.networkType


class CurrentAlarmSensor(GeneracEntity, SensorEntity):
    """Current Alarm sensor from v5 API."""

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{DEFAULT_NAME}_{self.generator_id}_current_alarm"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self.aparatus_detail.currentAlarm


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
