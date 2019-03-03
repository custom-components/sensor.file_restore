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

__version__ = '1.0.0'

ATTR_TEMPERATURES = 'temperature_programs'

CONF_FILE_PATH = 'file_path'
CONF_UNIT_OF_MEASUREMENT = 'unit_of_measurement'

DEFAULT_NAME = 'File_restore'
ICON = 'mdi:file'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_FILE_PATH): cv.isfile,
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
    vol.Optional(CONF_UNIT_OF_MEASUREMENT): cv.string,
})


async def async_setup_platform(hass, config, async_add_entities,
                               discovery_info=None):
    """Set up the file sensor."""
    file_path = config.get(CONF_FILE_PATH)
    name = config.get(CONF_NAME)
    unit = config.get(CONF_UNIT_OF_MEASUREMENT)

    if hass.config.is_allowed_path(file_path):
        async_add_entities(
            [FileSensor(name, file_path, unit)], True)
    else:
        _LOGGER.error("'%s' is not a whitelisted directory", file_path)


class FileSensor(Entity):
    """Implementation of a file sensor."""

    def __init__(self, name, file_path, unit):
        """Initialize the file sensor."""
        self._name = name
        self._file_path = file_path
        self._state = None
        self._unit = unit
        self._temperatures = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

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
            ATTR_TEMPERATURES: self._temperatures
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
            self._temperatures[index] = float(data_array[index])

        hour = datetime.now().hour
        day = datetime.now().weekday()
        self._state = self._temperatures[24 * day + hour]
