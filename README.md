# rpi-temp

## The problem

I want to use a Raspberry Pi to measure the outside temperature over time. I
want to be able to access the data without having to connect to the Raspberry Pi
in any way because it will be running on a home network with a dynamic IP.

I want to be able to visualise the temperature data in different ways easily and
possibly add additional sensors such as for rainfall in future.

## What this code does

Writes a datapoint (e.g. the current temperature) to some location (e.g. a file
or API) along with a timestamp, repeating after a certain period of seconds.

I am using this to write the current temperature from a Raspberry Pi thermometer
to a Google spreadsheet at a specified time interval. However, it could be used
to write any time sensitive data to any location. I've chosen Google Sheets
because it has a robust API and it's free and simple.

Different modules can be used to specify what data is recorded and where it is
written. This is so that I can connect additional sensors to write to a 
different API without having to drastically change the code in future.

Loads two modules from the root folder of the codebase:
- a data point module to fetch a data point from a sensor such as a thermometer.
- a persistence module to write this data somewhere with a timestamp, for
example to a local file or a Google spreadsheet via the Google API.

The modules used are specified by setting environment variables. Alternative
data point or persistence modules can be added to this folder.

For the Raspberry Pi thermometer I load the temperature.py module to fetch a
temperature data point and the googlesheets.py module to write the datapoint to
the Google Sheets API. I also set the period between datapoints to 60 seconds. 
This is how it's run manually at the command line:

`PERSISTENCEMOD="googlesheets" DATAPOINTMOD="temperature" DATAPOINTPERIOD=60 python timedatapoints.py`

## Setup

### Set up Google Sheets API authentication

I'm using Google Sheets API because it's free and has a simple API.

1. Go to https://console.cloud.google.com
2. Set up a project
3. Export credentials to a file and rename it key.json.
4. Copy key.json to this folder.

Based on https://hands-on.cloud/python-google-sheets-api/?utm_content=cmp-true
which also describes how to set up the Google API for this to work.

### Set up 1-wire interface on the Raspberry Pi
This is required if the plugin you're using reads data from a 1-wire device.
https://www.raspberrypi-spy.co.uk/2018/02/enable-1-wire-interface-raspberry-pi/

### Redis Queue
I wanted to queue requests to the Google Sheets API so that if the Raspberry Pi
goes off line requests will be queued up until the connection is restored.

The file and googlesheets persistence class modules use Redis Queue, which will
need to be installed on the Raspberry Pi:

`sudo apt-get install redis-server`

A redis queue worker will also need to be running. **This should be run from the
root folder of this codebase:**

`rq worker --with-scheduler`

### Services
To run robustly and restart when the Raspberry Pi is rebooted I found it best to
run the Redis Queue and timedatapoints.py as a service.

#### Running Redis Queue as a service

```
sudo cp rqworker@.service /lib/systemd/system/rqworker@.service
sudo systemctl daemon-reload
sudo systemctl enable rqworker@1
sudo systemctl start rqworker@1
```

#### Running timedatapoints.py as a service

```
sudo cp timedatapoints.service /lib/systemd/system/timedatapoints.service
sudo systemctl daemon-reload
sudo systemctl enable timedatapoints.service
sudo systemctl start timedatapoints.service
```

### Plugin modules
Additional modules can be added to provide different persistence and datapoint
functionality. Just change the values of PERSISTENCEMOD and DATAPOINTMOD to
contain the name of the module.

Datapoint modules must implement a function called write().
Persistence modules must implement a function called get().

## Monitoring

I use https://healthchecks.io as a simple and free way of being alerted if the
Raspberry Pi goes off line. It works by setting up a cron job on the Raspberry
Pi that pings a healthchecks.io URL every few minutes. If, after a certain
period a ping is not received, then I receive an alert via email and WhatsApp
and I can investigate the problem.

## A front end

Data sent to the Google Sheets API can easily be viewed, shared with other
people and used to plot graphs. However, I realised that I wanted to see a few
things at a glance, e.g, latest temperature recorded, maximum and minimum 
temperature over the last 24 hours.

I don't want to pay for any hosting services, so I built a simple React app that
runs for free on Github pages. 

The repository for the front end is here: https://github.com/edwardcrompton/weather-frontend

The front end can be viewed here: https://edwardcrompton.github.io/weather-frontend/
