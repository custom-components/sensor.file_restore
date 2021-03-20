""" Useful constant for file_restore integration """
#Generic
VERSION = "4.1"
DOMAIN = "file_restore"
PLATFORM = "sensor"
ISSUE_URL = "https://github.com/custom-components/sensor.file_restore/issues"
CONFIGFLOW_VERSION = 2

#Defaults
DEFAULT_NAME = 'file_restore'
DEFAULT_LENGTH = 'week'
DEFAULT_DETAIL = 'hour'
ICON = 'mdi:file'

#Attributes
ATTR_TEMPERATURES = 'program_values'

#Time constant
CON_YEAR = "year"
CON_MONTH = "month"
CON_WEEK = "week"
CON_DAY = "day"
CON_HOUR = "hour"
CON_MINUTE = "minute"

#Options
LENGTH_OPTIONS = [CON_YEAR, CON_MONTH, CON_WEEK, CON_DAY, CON_HOUR]
DETAL_OPTIONS_FULL = [CON_MONTH, CON_WEEK, CON_DAY, CON_HOUR, CON_MINUTE]
DETAIL_OPTIONS_YEAR = [CON_MONTH, CON_WEEK, CON_DAY]
DETAIL_OPTIONS_MONTH = [CON_DAY, CON_HOUR]
DETAIL_OPTIONS_WEEK = [CON_DAY, CON_HOUR]
DETAIL_OPTIONS_DAY = [CON_HOUR, CON_MINUTE]
DETAIL_OPTIONS_HOUR = [CON_MINUTE]
