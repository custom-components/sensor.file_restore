# FILE RESTORE

This component is a revision of the official Home Assistant component 'File Sensor' in order to have specifica function to program the value during the day.
The component include also a special attribute that include the all the value read from the file configured in the setup.

`file_restore` component has been developed to fulfill the need of a Home Assistant object that is able to return a different value according to time, for example you can get a different value each hour within a week.
In other word this will allow you to define a program of value that will change with time and repeat when reached the last value. In this way you can use that value to do actions accordingly.

## HOW TO INSTALL
Just copy paste the content of the `sensor.file_restore/custom_components` folder in your `config/custom_components` directory.

As example you will get the '.py' file in the following path: `/config/custom_components/file_restore/sensor.py`.

Note: This can be install through HACS

## EXAMPLE OF SETUP
Here below the example of setup of sensor and parameters to configure.

```yaml
sensor:
  - platfrom: file_restore
    unit_of_measurement: '°C'
    file_path: {path}/file.txt
    name: File
    length: month
    detail: day
```

Field | Value | Necessity | Comments
--- | --- | --- | ---
platform | `file_restore` | *Required* |
unit_of_measurement |  | Optional |
file_path |  | *Required* | path of the file. Be sure that the URL is whitelisted, if needed.
name | File_restore | Optional |
length | week | Optional | this define the length of the period. Possibile combinantion of length and detail below.
detail | hour | Optional | this define the detail of the period. Possibile combinantion of length and detail below.

## SPECIFICITIES
### DATA FILE
File defined in `file_path` must have the structure of a CSV file with value separated by a comma. The list of data is composed by the number of elements in the table below. This table shows also the possibile combinantion of data.

Length | Detail | Number of elements | Note
--- | --- | --- | ---
hour | minute | 60 | This will change the value each minute and will restart form the first value each hour.
day | minute | 1440 | This will change the value each minute and will restart from the first value each day.
day | hour | 24 | This will change the value each hour and will restart from the first value each day.
week | hour | 168 | This will change the value each hour and will restart from the first value each week.
week | day | 7 | This will change the value each day and will restart from the first value each week.
month | hour | 744 | This will change the value each hour and will restart from the first value each month.
month | day | 31 | This will change the value each day and will restart from the first value each month.
year | day | 366 | This will change the value each day and will restart from the first value each year.
year | week | 53 | This will change the value each week and will restart from the first value each year.
year | month | 12 | This will change the value each month and will restart from the first value each year.

NOTE:
- Week is counted from Monday to Sunday (ISO week).
- First day of the year is Jan-01
- First week of the year is the one that include at least 4 days (ISO definition)
- Only last line of file will be read.
- Data in the CSV file has to be numbers.

To give you an example:
```csv
10.0, 10.5, ...(165 other values)..., 11.0
```
### ATTRIBUTE AND STATE
Attribute `program_values` that include all values read from the file.
State of the sensor will change automatically according the the data read from file.

## NOTE
This component has been developed for the bigger project of building a smart thermostat using Home Assistant and way cheeper then the commercial ones.
You can find more infomration [here][2].

***
Due to how `custom_components` are loaded, it could be possible to have a `ModuleNotFoundError` error on first boot after adding this; to resolve it, restart Home-Assistant.

***
![logo][1]

[1]: https://github.com/MapoDan/home-assistant/blob/master/mapodanlogo.png
[3]: https://github.com/MapoDan/home-assistant
