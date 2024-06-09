# rpi-temp

Wrapper for the Raspberry Pi temperature monitor

Loads two classes in modules within the plugins folder:

 - A data point class. This is used to fetch the datapoint we want to write somewhere with a timestamp.

 - A persistence class. This is used to write the datapoint and the timestamp somewhere where it will be persisted, e.g the Google Sheets API.

## Setup

### Set the modules and classnames for the environment.
`export PERSISTENCECLASS="googlesheets.PersistToGoogleSheets"`

`export DATAPOINTCLASS="temperature.Temperature"`

### Set up Google Sheets API authentication
Go to https://console.cloud.google.com
Set up a project
Export credentials to a file and rename it key.json in this folder.

### Set up 1-wire interface
This is required if the plugin you're using reads data from a 1-wire device.
https://www.raspberrypi-spy.co.uk/2018/02/enable-1-wire-interface-raspberry-pi/

## Running
`python timedatapoints.py`

Based on https://hands-on.cloud/python-google-sheets-api/?utm_content=cmp-true which also describes how to get up the Google API for this to work.

### Plugins
Additional modules can be added to the plugins directory to provide different persistence and datapoint classes. Just change the values of PERSISTENCECLASS and DATAPOINTCLASS to point to the plugin using the format `<modulename>.<classname>`.

The classes must be instances of the datapointinterface or the persistenceinterface abstract classes.

