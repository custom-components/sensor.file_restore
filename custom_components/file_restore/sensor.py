"""
Support for sensor that get the value of a text value of a strinng of temperature value for the programmable thermostat.
"""
import os
import logging
import json

import voluptuous as vol

import homeassistant.helpers.config_validation as cv
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import (
    CONF_VALUE_TEMPLATE, CONF_NAME, CONF_UNIT_OF_MEASUREMENT)
from homeassistant.helpers.entity import Entity
from datetime import datetime

_LOGGER = logging.getLogger(__name__)

__version__ = '2.0'

ATTR_TEMPERATURES = 'program_values'

CONF_FILE_PATH = 'file_path'
CONF_UNIT_OF_MEASUREMENT = 'unit_of_measurement'
CONF_LENGTH = 'length'
CONF_DETAIL = 'detail'

DEFAULT_NAME = 'file_restore'
DEFAULT_LENGTH = 'week'
DEFAULT_DETAIL = 'hour'
ICON = 'mdi:file'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_FILE_PATH): cv.isfile,
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
    vol.Optional(CONF_UNIT_OF_MEASUREMENT): cv.string,
    vol.Optional(CONF_DETAIL, default=DEFAULT_DETAIL): cv.string,
    vol.Optional(CONF_LENGTH, default=DEFAULT_LENGTH): cv.string
})


async def async_setup_platform(hass, config, async_add_entities,
                               discovery_info=None):
    """Set up the file sensor."""
    file_path = config.get(CONF_FILE_PATH)
    name = config.get(CONF_NAME)
    unit = config.get(CONF_UNIT_OF_MEASUREMENT)
    length_s = config.get(CONF_LENGTH)
    detail_s = config.get(CONF_DETAIL)
    month = 1
    week = 1
    day = 1
    hour = 1
    minute = 1
    """This is to define the amout of data that has to be managed"""
    if length_s == 'hour' and detail_s == 'minute':
        minute = 60
    elif length_s == 'day' and detail_s == 'minute':
        hour = 24
        minute = 60
    elif length_s == 'day' and detail_s == 'hour':
        hour = 24
    elif length_s == 'week' and detail_s == 'hour':
        day = 7
        hour = 24
    elif length_s == 'week' and detail_s == 'day':
        day = 7
    elif length_s == 'month' and detail_s == 'hour':
        day = 31
        hour = 24
    elif length_s == 'month' and detail_s == 'day':
        day = 31
    elif length_s == 'year' and detail_s == 'day':
        day = 366
    elif length_s == 'year' and detail_s == 'week':
        week = 53
    elif length_s == 'year' and detail_s == 'month':
        month = 12
    else:
        _LOGGER.error("Parameters has a not acceptable value, check possibile values of length and detail")


    if hass.config.is_allowed_path(file_path):
        async_add_entities(
            [FileSensor(name, file_path, unit, month, week, day, hour, minute, length_s, detail_s)], True)
    else:
        _LOGGER.error("'%s' is not a whitelisted directory", file_path)


class FileSensor(Entity):
    """Implementation of a file sensor."""

    def __init__(self, name, file_path, unit, month, week, day, hour, minute, length, detail):
        """Initialize the file sensor."""
        self._name = name
        self._file_path = file_path
        self._state = None
        self._unit = unit
        self._month = month
        self._week = week
        self._day = day
        self._hour = hour
        self._minute = minute
        self._length = length
        self._detail = detail
        self._program = [0]*(self._month * self._week * self._day * self._hour * self._minute)

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
            _LOGGER.warning("File or data not present at the moment: %s",
                            os.path.basename(self._file_path))
            return

        data_array = data.split(',')
        for index in range(len(data_array)):
            self._program[index] = float(data_array[index])

        # Retrive time and date data for calculation
        month = datetime.now().month
        hour = datetime.now().hour
        minute = datetime.now().minute
        if self._day == 366:
            day = int(datetime.strftime(datetime.now(),'%j'))
        elif self._day == 7:
            day = datetime.now().weekday()
        else:
            day = datetime.now().day
        week = datetime.now().isocalendar()[1]

        # Calculate position
        if self._length == 'hour' and self._detail == 'minute':
            position = minute
        elif self._length == 'day' and self._detail == 'minute':
            position = 60 * hour + minute
        elif self._length == 'day' and self._detail == 'hour':
            position = hour
        elif self._length == 'week' and self._detail == 'hour':
            position = 24 * day + hour
        elif self._length == 'week' and self._detail == 'day':
            position = day
        elif self._length == 'month' and self._detail == 'hour':
            position = 24 * (day - 1) + hour # the -1 is required becasue in this case day range is between 1 and 31 (and not from 0)
        elif self._length == 'month' and self._detail == 'day':
            position = day
        elif self._length == 'year' and self._detail == 'day':
            position = day
        elif self._length == 'year' and self._detail == 'week':
            position = week
        elif self._length == 'year' and self._detail == 'month':
            position = month
        self._state = self._program[position]
