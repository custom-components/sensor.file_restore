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
from .utilities import (
    create_file_and_directory,
    null_data_cleaner
)
from .const import (
    DOMAIN,
    CONFIGFLOW_VERSION
)
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

#####################################################
#################### CONFIG FLOW ####################
#####################################################
@config_entries.HANDLERS.register(DOMAIN)
class FileRestoreConfigFlow(config_entries.ConfigFlow):
    """File Restore config flow."""

    VERSION = CONFIGFLOW_VERSION
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    def __init__(self):
        """Initialize."""
        self._errors = {}
        self._data = {}
        self._unique_id = str(uuid.uuid4())

    """ INITIATE CONFIG FLOW """
    async def async_step_user(self, user_input={}):
        """User initiated config flow."""
        self._errors = {}
        if user_input is not None:
            if are_first_step_data_valid(self, user_input):
                self._data.update(user_input)
                _LOGGER.info("First input data are valid. Proceed with final step. %s", self._data)
                return await self.async_step_final()
            _LOGGER.warning("Wrong data have been input in the first form")
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
        self._errors = {}
        if user_input is not None and user_input != {}:
            self._data.update(user_input)
            final_data = {}
            for key in self._data.keys():
                if self._data[key] != "" and self._data[key] != []:
                    final_data.update({key: self._data[key]})
            _LOGGER.info("Data are valid. Proceed with entity creation. - %s", final_data)
            await self.async_set_unique_id(self._unique_id)
            self._abort_if_unique_id_configured()
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

    """ SHOW CONFIGURATION.YAML ENTITIES """
    async def async_step_import(self, user_input):
        """Import a config entry.
        Special type of import, we're not actually going to store any data.
        Instead, we're going to rely on the values that are in config file."""

        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")

        return self.async_create_entry(title="configuration.yaml", data={})

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        if config_entry.unique_id is not None:
            return OptionsFlowHandler(config_entry)
        else:
            return EmptyOptions(config_entry)

#####################################################
#################### OPTION FLOW ####################
#####################################################
class OptionsFlowHandler(config_entries.OptionsFlow):
    """File Restore config flow."""

    def __init__(self, config_entry):
        """Initialize."""
        self._errors = {}
        self._data = {}
        self.config_entry = config_entry
        if self.config_entry.options == {}:
            self._data.update(self.config_entry.data)
        else:
            self._data.update(self.config_entry.options)
        _LOGGER.debug("_data to start options flow: %s", self._data)

    """ INITIATE CONFIG FLOW """
    async def async_step_init(self, user_input={}):
        """User initiated config flow."""
        self._errors = {}
        if user_input is not None:
            if are_first_step_data_valid(self, user_input):
                self._data = null_data_cleaner(self._data, user_input)
                _LOGGER.info("First input data are valid. Proceed with final step. %s", self._data)
                return await self.async_step_final()
            _LOGGER.warning("Wrong data have been input in the first form")
            return await self._show_config_form_first(user_input)
        return await self._show_config_form_first(user_input)

    """ SHOW FIRST FORM """
    async def _show_config_form_first(self, user_input):
        """ Show form for config flow """
        _LOGGER.info("Show first form %s", user_input)
        if user_input is None or user_input == {}:
            user_input = self._data
        #3 is necessary for options. Check config_schema.py for explanations.
        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(get_config_flow_schema(user_input, 3, "")),
            errors=self._errors
        )

    """ LAST CONFIG FLOW STEP """
    async def async_step_final(self, user_input={}):
        """User initiated config flow."""
        self._errors = {}
        if user_input is not None and user_input != {}:
            self._data = null_data_cleaner(self._data, user_input)
            final_data = {}
            for key in self._data.keys():
                if self._data[key] != "" and self._data[key] != []:
                    final_data.update({key: self._data[key]})
            _LOGGER.info("Data are valid. Proceed with entity creation. - %s", final_data)
            return self.async_create_entry(title="", data=final_data)
        return await self._show_config_form_final(user_input)

    """ SHOW LAST FORM """
    async def _show_config_form_final(self, user_input):
        """ Show form for config flow """
        _LOGGER.info("Show final form")
        if user_input is None or user_input == {}:
            user_input = self._data
        return self.async_show_form(
            step_id="final",
            data_schema=vol.Schema(get_config_flow_schema(user_input, 2, self._data[CONF_LENGTH])),
            errors=self._errors
        )

    """ SHOW CONFIGURATION.YAML ENTITIES """
    async def async_step_import(self, user_input):
        """Import a config entry.
        Special type of import, we're not actually going to store any data.
        Instead, we're going to rely on the values that are in config file."""

        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")

        return self.async_create_entry(title="configuration.yaml", data={})

#####################################################
#################### EMPTY  FLOW ####################
#####################################################
class EmptyOptions(config_entries.OptionsFlow):
    """A class for default options. Not sure why this is required."""

    def __init__(self, config_entry):
        """Just set the config_entry parameter."""
        self.config_entry = config_entry

#####################################################
############## DATA VALIDATION FUCTION ##############
#####################################################
def are_first_step_data_valid(self, user_input) -> bool:
    if user_input[CONF_FILE_PATH] == "":
        self._errors["base"]="file_path_empty"
        return False
    else:
        user_input[CONF_FILE_PATH] = user_input[CONF_FILE_PATH].replace("\\", "/")
        if user_input[CONF_FILE_PATH][0]=="/":
            user_input[CONF_FILE_PATH] = user_input[CONF_FILE_PATH][1::]
        user_input[CONF_FILE_PATH] = user_input[CONF_FILE_PATH].replace("local/", "www/")
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
            if CONF_NAME in user_input:
                create_file_and_directory(user_input[CONF_FILE_PATH], user_input[CONF_NAME])
            else:
                create_file_and_directory(user_input[CONF_FILE_PATH], self._data[CONF_NAME])
    return True
