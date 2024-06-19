# rpi-temp

Wrapper for the Raspberry Pi temperature monitor

Loads modules from the plugins folder:

 - A data point module. This is used to fetch the datapoint we want to write
somewhere with a timestamp.

 - A persistence module. This is used to write the datapoint and the timestamp
somewhere where it will be persisted, e.g the Google Sheets API.

## Setup

### Set the modules names for the environment.
`export PERSISTENCEMOD="googlesheets"`

`export DATAPOINTMOD="temperature"`

### Set up Google Sheets API authentication
Go to https://console.cloud.google.com
Set up a project
Export credentials to a file and rename it key.json. Put it in the plugins
folder.

### Set up 1-wire interface
This is required if the plugin you're using reads data from a 1-wire device.
https://www.raspberrypi-spy.co.uk/2018/02/enable-1-wire-interface-raspberry-pi/

### Redis Queue
If the persistence class plugin you are using uses Redis Queue, that will need
to be installed on the system:

`sudo apt-get install redis-server`

A redis queue worker will also need to be running. This should be set up to run
on boot of the system:

`rq worker --with-scheduler`

## Running
`python timedatapoints.py`

Based on https://hands-on.cloud/python-google-sheets-api/?utm_content=cmp-true
which also describes how to get up the Google API for this to work.

### Plugins
Additional modules can be added to the plugins directory to provide different
persistence and datapoint functionality. Just change the values of
PERSISTENCEMOD and DATAPOINTMOD to contain the name of the module.

Datapoint modules must implement a function called write().
Persistence plugins must implement a function called get().
