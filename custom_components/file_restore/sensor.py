"""
Support for sensor that get the value of a text value of a strinng of temperature value for the programmable thermostat.
"""
import os
import logging
import json

from homeassistant.config_entries import SOURCE_IMPORT
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import (
    CONF_VALUE_TEMPLATE,
    CONF_NAME,
    CONF_UNIT_OF_MEASUREMENT
)
from homeassistant.helpers.entity import Entity
from datetime import datetime
from .const import (
    VERSION,
    DOMAIN,
    PLATFORM,
    ATTR_TEMPERATURES,
    CON_YEAR,
    CON_MONTH,
    CON_WEEK,
    CON_DAY,
    CON_HOUR,
    CON_MINUTE,
    ICON
)
from .config_schema import (
    SENSOR_SCHEMA,
    CONF_FILE_PATH,
    CONF_UNIT_OF_MEASUREMENT,
    CONF_LENGTH,
    CONF_DETAIL
)
from .utilities import create_file_and_directory

_LOGGER = logging.getLogger(__name__)

__version__ = VERSION

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(SENSOR_SCHEMA)

async def async_setup_platform(hass, config, async_add_entities,
                               discovery_info=None):
    """Set up the file sensor."""
    _LOGGER.debug("Setup entity coming from configuration.yaml named: %s", config.get(CONF_NAME))
    async_add_entities([FileSensor(config)], True)

async def async_setup_entry(hass, config_entry, async_add_devices):
    """Add file sensor entities from configuration flow."""
    _LOGGER.debug("setup entity-config_entry_data=%s",config_entry.data)
    async_add_devices([FileSensor(config_entry.data)], True)

class FileSensor(Entity):
    """Implementation of a file sensor."""

    def __init__(self, config):
        """Initialize the file sensor."""
        self._name = config.get(CONF_NAME)
        self._file_path = config.get(CONF_FILE_PATH)
        self._state = None
        self._unit = config.get(CONF_UNIT_OF_MEASUREMENT)
        self._length = config.get(CONF_LENGTH)
        self._detail = config.get(CONF_DETAIL)

        """This is to define the amout of data that has to be managed"""
        time_data = self.get_value_according_to_length_detail()
        self._program = [0]*(time_data[1] * time_data[2] * time_data[3]  * time_data[4]  * time_data[5])


    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def unit_of_measurement(self):
        """Return the unit the value is expressed in."""
        return self._unit

    @property
    def icon(self):
        """Return the icon to use in the frontend, if any."""
        return ICON

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def device_state_attributes(self):
        """Return the state attributes of the sensor."""
        return {
            ATTR_TEMPERATURES: self._program
        }

    def update(self):
        """Get the latest entry from a file and updates the state."""
        try:
            with open(self._file_path, 'r', encoding='utf-8') as file_data:
                for line in file_data:
                    data = line
                data = data.strip()
        except (IndexError, FileNotFoundError, IsADirectoryError,
                UnboundLocalError):
            create_file_and_directory(self._file_path, self._name)

        try:
            data_array = data.split(',')
            for index in range(len(data_array)):
                self._program[index] = float(data_array[index])
        except:
            _LOGGER.warning("sensor.%s - File doesn't include valid data. Set to all 0.", self._name)

        self._state = self._program[self.get_value_according_to_length_detail()[0]]

    def get_value_according_to_length_detail(self):
        month = datetime.now().month
        hour = datetime.now().hour
        minute = datetime.now().minute
        if self._length == CON_YEAR and self._detail == CON_DAY:
            day = int(datetime.strftime(datetime.now(),'%j'))
        elif self._length == CON_WEEK:
            day = datetime.now().weekday()
        else:
            day = datetime.now().day
        week = datetime.now().isocalendar()[1]
        #Return array data are [position, month, week, day, hour, minute]
        if self._length == CON_HOUR and self._detail == CON_MINUTE:
            return [minute, 1, 1, 1, 1, 60]
        elif self._length == CON_DAY and self._detail == CON_MINUTE:
            return [60 * hour + minute, 1, 1, 1, 24, 60]
        elif self._length == CON_DAY and self._detail == CON_HOUR:
            return [hour, 1, 1, 1, 24, 1]
        elif self._length == CON_WEEK and self._detail == CON_HOUR:
            return [24 * day + hour, 1, 1, 7, 24, 1]
        elif self._length == CON_WEEK and self._detail == CON_DAY:
            return [day, 1, 1, 7, 1, 1]
        elif self._length == CON_MONTH and self._detail == CON_HOUR:
            return [24 * (day - 1) + hour, 1, 1, 31, 24, 1]
            # the -1 is required becasue in this case day range is between 1 and 31 (and not from 0)
        elif self._length == CON_MONTH and self._detail == CON_DAY:
            return [day, 1, 1, 31, 1, 1]
        elif self._length == CON_YEAR and self._detail == CON_DAY:
            return [day, 1, 1, 366, 1, 1]
        elif self._length == CON_YEAR and self._detail == CON_WEEK:
            return [week, 1, 53, 1, 1, 1]
        elif self._length == CON_YEAR and self._detail == CON_MONTH:
            return [month, 12, 1, 1, 1, 1]
        else:
            _LOGGER.error("Parameters has a not acceptable value, check possibile values of length and detail on documentation")
            return []
