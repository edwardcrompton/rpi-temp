import os
import importlib
import importlib.machinery
import importlib.util
import sys
import time
from pathlib import Path

def main():
    # Get environment configuration
    # @todo Let's make these arguments passed when the python script is called
    # instead of environment variables?
    datapointmod = os.environ.get('DATAPOINTMOD')
    persistencemod = os.environ.get('PERSISTENCEMOD')
    period = os.environ.get('DATAPOINTPERIOD')
    
    if datapointmod is None or persistencemod is None:
        if datapointmod is None:
            print('Please add the DATAPOINTMOD env var.')
    
        if persistencemod is None:
            print('Please add the PERSISTENCEMOD env var.')
        
        quit()

    if period is None or period == 0:
        print('Please add the DATAPOINTPERIOD env var.')

        quit()

    # Load the datapoint class
    datapoint = dynamic_imp(datapointmod)

    # Load the persistence class
    persistence = dynamic_imp(persistencemod)

    # Set the logging period
    period = int(period)

    # Get the datapoint and write it to the persistence every number of seconds
    # defined by the period variable.
    starttime = time.monotonic()
    previous_job = None
    while True:
        job = execute(datapoint, persistence, previous_job)
        previous_job = job
        time.sleep(period - ((time.monotonic() - starttime) % period))

# dynamic import  
def dynamic_imp(name): 

    try:
        mod = __import__(name)
        return mod

    except ImportError: 
        print ("module not found: " + name)


def execute(datapoint, persistence, previous_job):
    current_time = time.localtime()
    formatted_time = time.strftime('%Y-%m-%d %H:%M', current_time)
    return persistence.write(formatted_time, datapoint.get(), previous_job)

# Function Call
if __name__ == '__main__':
    main()
