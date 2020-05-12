""" Configuration schema description for file_restore integration """
import voluptuous as vol
import logging
import homeassistant.helpers.config_validation as cv
from homeassistant.const import CONF_NAME
from .const import (
    DEFAULT_NAME,
    DEFAULT_LENGTH,
    DEFAULT_DETAIL,
    CON_YEAR,
    CON_MONTH,
    CON_WEEK,
    CON_DAY,
    CON_HOUR,
    CON_MINUTE,
    LENGTH_OPTIONS,
    DETAL_OPTIONS_FULL,
    DETAIL_OPTIONS_YEAR,
    DETAIL_OPTIONS_MONTH,
    DETAIL_OPTIONS_WEEK,
    DETAIL_OPTIONS_DAY,
    DETAIL_OPTIONS_HOUR,
    ICON
)

CONF_FILE_PATH = 'file_path'
CONF_UNIT_OF_MEASUREMENT = 'unit_of_measurement'
CONF_LENGTH = 'length'
CONF_DETAIL = 'detail'

SENSOR_SCHEMA = {
    vol.Required(CONF_FILE_PATH): cv.isfile,
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
    vol.Optional(CONF_UNIT_OF_MEASUREMENT): cv.string,
    vol.Optional(CONF_DETAIL, default=DEFAULT_DETAIL): vol.In(DETAL_OPTIONS_FULL),
    vol.Optional(CONF_LENGTH, default=DEFAULT_LENGTH): vol.In(LENGTH_OPTIONS)
}

def get_config_flow_schema(config: dict = {}, config_flow_step: int = 0, length_value: str = DEFAULT_LENGTH) -> dict:
    if not config:
        config = {
            CONF_NAME: DEFAULT_NAME,
            CONF_FILE_PATH: "",
            CONF_UNIT_OF_MEASUREMENT: "",
            CONF_LENGTH: DEFAULT_LENGTH,
            CONF_DETAIL: DEFAULT_DETAIL
        }
    if config_flow_step==1:
        return {
            vol.Optional(CONF_NAME, default=DEFAULT_NAME): str,
            vol.Required(CONF_FILE_PATH): str,
            vol.Optional(CONF_UNIT_OF_MEASUREMENT): str,
            vol.Optional(CONF_LENGTH, default=DEFAULT_LENGTH): vol.In(LENGTH_OPTIONS)
        }
    elif config_flow_step==2 and length_value==CON_YEAR:
        return {
            vol.Required(CONF_DETAIL): vol.In(DETAIL_OPTIONS_YEAR)
        }
    elif config_flow_step==2 and length_value==CON_MONTH:
        return {
            vol.Required(CONF_DETAIL): vol.In(DETAIL_OPTIONS_MONTH)
        }
    elif config_flow_step==2 and length_value==CON_WEEK:
        return {
            vol.Optional(CONF_DETAIL, default=DEFAULT_DETAIL): vol.In(DETAIL_OPTIONS_WEEK)
        }
    elif config_flow_step==2 and length_value==CON_DAY:
        return {
            vol.Required(CONF_DETAIL): vol.In(DETAIL_OPTIONS_DAY)
        }
    elif config_flow_step==2 and length_value==CON_HOUR:
        return {
            vol.Required(CONF_DETAIL): vol.In(DETAIL_OPTIONS_HOUR)
        }

    return {}
