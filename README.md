# FILE RESTORE

This component is a revision of the official Home Assistant component 'File Sensor' in order to have specifica function to program the value during the day.
The component include also a special attribute that include the all the value read from the file configured in the setup.

`file_restore` component has been developed to fulfill the need of a Home Assistant object that is able to return a value different per each hour and day of in a week with also the custom attribute that was necessary for my scope.

## HOW TO INSTALL
Just copy paste the content of the `sensor.file_restore/custom_components` folder in your `config/custom_components` directory.

As example you will get the '.py' file in the following path: `/config/custom_components/file_restore/sensor.py`.

## EXAMPLE OF SETUP
```yaml
sensor:
  - platfrom: file_restore
    unit_of_measurement: '°C'
    file_path: {path}/file.txt
    name: File
```

Field | Value | Necessity | Comments
--- | --- | --- | ---
platform | `file_restore` | *Required* |
unit_of_measurement |  | Optional |
file_path |  | *Required* | path of the file. Be sure that the URL is whitelisted, if needed.
name| File_restore | Optional |

## SPECIFICITIES
### DATA FILE
File defined in `file_path` must have the structure of a CSV file with value separated by a comma. The list of data is composed by 168 elements, one per each hour in a week and ordered within the week.

NOTE:
- Week is counted from Monday to Sunday (ISO week).
- Only last line of file will be read.

To give you an example:
```csv
10.0, 10.5, ...(165 other values)..., 11.0
```
### ATTRIBUTE AND STATE
Attribute `temperature_program` that include all 168 values read from the file.
State of the the sensor will change automatically according the the data read from file.

## NOTE
This component has been developed for the bigger project of building a smart thermostat using Home Assistant and way cheeper then the commercial ones.
You can find more infomration [here][2].

***
Due to how `custom_components` are loaded, it could be possible to have a `ModuleNotFoundError` error on first boot after adding this; to resolve it, restart Home-Assistant.

***
![logo][1]

[1]: https://github.com/MapoDan/home-assistant/blob/master/mapodanlogo.png
[3]: https://github.com/MapoDan/home-assistant
