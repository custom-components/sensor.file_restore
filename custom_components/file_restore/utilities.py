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
