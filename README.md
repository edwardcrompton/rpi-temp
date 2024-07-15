# rpi-temp

Writes a datapoint (e.g. the current temperature) to some location (e.g. a file
or API) along with a timestamp, repeating after a certain period of seconds.

For example, this can be used to write the current temperature from a raspberry
pi thermometer to a Google spreadsheet at a specified time interval. However,
it could be used to write any time sensitive data to any location.

Different modules can be used to specify what data is recorded and where it is
written.

Loads two modules from this folder:
- a datapoint module to fetch a datapoint from some logic or a sensor such as a
thermometer.
- a persistence module to write this data somewhere with a timestamp, for
example to a local file or a Google spreadsheet via the Google API.

The modules are specified at run time. Additional datapoint or persistence
modules can be added to this folder.

## Example commands
These commands are available with the current modules.

Write a timestamp and random number to a file:

`PERSISTENCEMOD="file" DATAPOINTMOD="number" python timedatapoints.py`

Write a timestamp and random number to a Google spreadsheet:

`PERSISTENCEMOD="googlesheets" DATAPOINTMOD="number" python timedatapoints.py`

Write a timestamp and the temperature read from an attached thermometer to a
Google spreadsheet:

`PERSISTENCEMOD="googlesheets" DATAPOINTMOD="temperature" python timedatapoints.py`

## Setup

### Set up Google Sheets API authentication
Go to https://console.cloud.google.com
Set up a project
Export credentials to a file and rename it key.json. Put it in the plugins
folder.

### Set up 1-wire interface
This is required if the plugin you're using reads data from a 1-wire device.
https://www.raspberrypi-spy.co.uk/2018/02/enable-1-wire-interface-raspberry-pi/

### Redis Queue
The file and googlesheets persistence class modules use Redis Queue, which will
need to be installed on the system:

`sudo apt-get install redis-server`

A redis queue worker will also need to be running. **This should be run from the
root folder of this codebase:**

`rq worker --with-scheduler`

or, as a service with

```
sudo cp rqworker@.service /lib/systemd/system/rqworker@.service
sudo systemctl daemon-reload
sudo systemctl enable rqworker@1
sudo systemctl start rqworker@1
```

## Running
`python timedatapoints.py`

Based on https://hands-on.cloud/python-google-sheets-api/?utm_content=cmp-true
which also describes how to get up the Google API for this to work.

### As a service

```
sudo cp timedatapoints.service /lib/systemd/system/timedatapoints.service
sudo systemctl daemon-reload
sudo systemctl enable hello.service
sudo systemctl start hello.service
```

### Plugin modules
Additional modules can be added to provide different persistence and datapoint
functionality. Just change the values of PERSISTENCEMOD and DATAPOINTMOD to
contain the name of the module.

Datapoint modules must implement a function called write().
Persistence modules must implement a function called get().
