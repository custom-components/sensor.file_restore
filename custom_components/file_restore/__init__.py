"""
This component is an upgraded version of file sensor.
It has the same characteristics but it:
  - expect a vecotr of data read from file in order to be able to interpret it.
  - vector is 24x7 elements long in order to cover all hours in a week starting from 00:00 of Monday to 23:00 of Sunday.
  - It has an additional property that return the whole vector read.
"""
