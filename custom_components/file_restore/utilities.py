import os
import logging

_LOGGER = logging.getLogger(__name__)

def create_file_and_directory(file_path, name) -> bool:
    data=f"File automatically generated with creation of file_restore entity {name}\n------------------------------------------------------------------------------\n"
    directory=file_path[:file_path.rfind("/"):]
    if not os.path.isdir(directory):
        os.mkdir(directory)
    with open(file_path, 'w', encoding='utf-8') as file_data:
        file_data.write(data)
    _LOGGER.info("File and/or directory was missing. Proceeded with creation.")
    return True

def null_data_cleaner(original_data: dict, data: dict) -> dict:
    """ this is to remove all null parameters from data that are added during option flow """
    for key in data.keys():
        if data[key] == "null":
            original_data[key] = ""
        else:
            original_data[key]=data[key]
    return original_data
