""" Configuration flow for the programmable_thermostat integration to allow user
    to define all file resotre entities from Lovelace UI."""
import logging
import os
from homeassistant.core import callback
import voluptuous as vol
import homeassistant.helpers.config_validation as cv
from homeassistant import config_entries
import uuid

from homeassistant.const import EVENT_HOMEASSISTANT_START
from .utilities import create_file_and_directory
from .const import DOMAIN
from homeassistant.const import CONF_NAME
from .config_schema import (
    get_config_flow_schema,
    SENSOR_SCHEMA,
    CONF_FILE_PATH,
    CONF_UNIT_OF_MEASUREMENT,
    CONF_LENGTH,
    CONF_DETAIL
)


_LOGGER = logging.getLogger(__name__)

@config_entries.HANDLERS.register(DOMAIN)
class FileRestoreConfigFlow(config_entries.ConfigFlow):
    """Programmable Thermostat config flow."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    def __init__(self):
        """Initialize."""
        self._errors = {}
        self._data = {}
        self._data["unique_id"] = str(uuid.uuid4())

    """ INITIATE CONFIG FLOW """
    async def async_step_user(self, user_input={}):
        """User initiated config flow."""
        self._errors = {}
        if user_input is not None:
            if self.are_first_step_data_valid(user_input):
                self._data.update(user_input)
                _LOGGER.info("First input data are valid. Proceed with final step. %s", self._data)
                return await self.async_step_final()
            _LOGGER.warning("Wrong date have been input in the first form")
            return await self._show_config_form_first(user_input)
        return await self._show_config_form_first(user_input)

    """ SHOW FIRST FORM """
    async def _show_config_form_first(self, user_input):
        """ Show form for config flow """
        _LOGGER.info("Show first form")
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(get_config_flow_schema(user_input, 1, "")),
            errors=self._errors
        )

    """ LAST CONFIG FLOW STEP """
    async def async_step_final(self, user_input={}):
        """User initiated config flow."""
        if user_input is not None and user_input != {}:
            self._data.update(user_input)
            final_data = {}
            for key in self._data.keys():
                if self._data[key] != "" and self._data[key] != []:
                    final_data.update({key: self._data[key]})
            _LOGGER.info("Data are valid. Proceed with entity creation. - %s", final_data)
            return self.async_create_entry(title=final_data["name"], data=final_data)
        return await self._show_config_form_final(user_input)

    """ SHOW LAST FORM """
    async def _show_config_form_final(self, user_input):
        """ Show form for config flow """
        _LOGGER.info("Show final form")
        return self.async_show_form(
            step_id="final",
            data_schema=vol.Schema(get_config_flow_schema(user_input, 2, self._data[CONF_LENGTH])),
            errors=self._errors
        )

    """ DATA VALIDATION FUCTIONS """
    def are_first_step_data_valid(self, user_input) -> bool:
        if user_input[CONF_FILE_PATH] == "":
            self._errors["base"]="file_path_empty"
            return False
        else:
            try:
                with open(user_input[CONF_FILE_PATH], 'r', encoding='utf-8') as file_data:
                    for line in file_data:
                        data = line
                    try:
                        data = data.strip()
                    except:
                        _LOGGER.warning("File is empty, please add some data in it.")
                        return True
            except (IndexError, FileNotFoundError, IsADirectoryError,
                    UnboundLocalError):
                create_file_and_directory(user_input[CONF_FILE_PATH], user_input[CONF_NAME])
        return True

    """ SHOW CONFIGURATION.YAML ENTITIES """
    async def async_step_import(self, user_input):
        """Import a config entry.
        Special type of import, we're not actually going to store any data.
        Instead, we're going to rely on the values that are in config file."""

        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")

        return self.async_create_entry(title="configuration.yaml", data={})
"""
    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        if config_entry.options.get("unique_id", None) is not None:
            return OptionsFlowHandler(config_entry)
        else:
            return EmptyOptions(config_entry)"""
