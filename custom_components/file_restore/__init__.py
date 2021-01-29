"""
This component is an upgraded version of file sensor.
It has the same characteristics but it:
  - expect a vecotr of data read from file in order to be able to interpret it.
  - vector lenght is dependant to information of setup.
  - It has an additional property that return the whole vector read.
"""
import os
import logging
import asyncio

from homeassistant import config_entries
from homeassistant.config_entries import (
    SOURCE_IMPORT,
    ConfigEntry
)
from homeassistant.helpers import discovery
from homeassistant.util import Throttle
from .sensor import FileSensor
from .const import (
    VERSION,
    DOMAIN,
    PLATFORM,
    ISSUE_URL,
    CONFIGFLOW_VERSION
)

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass, config):
    _LOGGER.info("Set up of integration %s, version %s, in case of issue open ticket at %s", DOMAIN, VERSION, ISSUE_URL)
    return True

async def async_setup_entry(hass, config_entry):
    """Set up this integration using UI."""
    if config_entry.source == config_entries.SOURCE_IMPORT:
        # We get here if the integration is set up using YAML
        hass.async_create_task(hass.config_entries.async_remove(config_entry.entry_id))
        return True
    undo_listener = config_entry.add_update_listener(update_listener)
    _LOGGER.info("Added new FileRestore entity, entry_id: %s", config_entry.entry_id)
    hass.async_create_task(hass.config_entries.async_forward_entry_setup(config_entry, PLATFORM))

    return True

async def async_unload_entry(hass, config_entry):
    """Unload a config entry."""
    _LOGGER.debug("async_unload_entry: %s", config_entry)
    await asyncio.gather(hass.config_entries.async_forward_entry_unload(config_entry, PLATFORM))
    return True

async def update_listener(hass, config_entry):
    """Handle options update."""
    _LOGGER.debug("update_listener: %s", config_entry)
    await hass.config_entries.async_reload(config_entry.entry_id)

async def async_migrate_entry(hass, config_entry: ConfigEntry):
    """Migrate old entry."""
    _LOGGER.debug("Migrating from version %s to version %s", config_entry.version, CONFIGFLOW_VERSION)

    new_data = {**config_entry.data}
    new_options = {**config_entry.options}

    if config_entry.version == 1:
        config_entry.unique_id = config_entry.data["unique_id"]
        del new_data["unique_id"]
        config_entry.version = CONFIGFLOW_VERSION
        config_entry.data = {**new_data}
        _LOGGER.info("Migration of entry %s done to version %s", config_entry.title, config_entry.version)
        return True

    _LOGGER.info("Migration not required")
    return True
