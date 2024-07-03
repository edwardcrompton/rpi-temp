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
    period = 60
    
    if datapointmod is None or persistencemod is None:
        if datapointmod is None:
            print('Please add the DATAPOINTMOD env var.')
    
        if persistencemod is None:
            print('Please add the PERSISTENCEMOD env var.')
        
        quit()

    # Load the datapoint class
    datapoint = dynamic_imp(datapointmod)

    # Load the persistence class
    persistence = dynamic_imp(persistencemod)

    # Get the datapoint and write it to the persistence every number of seconds
    # defined by the period variable.
    starttime = time.monotonic()
    while True:
        execute(datapoint, persistence)
        time.sleep(period - ((time.monotonic() - starttime) % period))

# dynamic import  
def dynamic_imp(name): 

    try:
        mod = __import__(name)
        return mod

    except ImportError: 
        print ("module not found: " + name)


def execute(datapoint, persistence):
    current_time = time.localtime()
    formatted_time = time.strftime('%Y-%m-%d %H:%M', current_time)
    persistence.write(formatted_time, datapoint.get())

# Function Call
if __name__ == '__main__':
    main()
