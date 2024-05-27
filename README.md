# rpi-temp

Wrapper for the Raspberry Pi temperature monitor

Loads two classes:
 - A data point class. This is used to fetch the datapoint we want to write somewhere with a timestamp.
 - A persistence class. This is used to write the datapoint and the timestamp somewhere where it will be persisted, e.g the Google Sheets API

## Setup

### Set the modules and classnames for the environment.
`export PERSISTENCECLASS="googlesheets.PersistToGoogleSheets"`
`export DATAPOINTCLASS="temperature.temperature"`

### Set up Google Sheets API authentication
Go to https://console.cloud.google.com
Set up a project
Export credentials to a file and rename it key.json in this folder

### Running
`python timedatapoints.py`

Based on https://hands-on.cloud/python-google-sheets-api/?utm_content=cmp-true which also describes how to get up the Google API for this to work.

