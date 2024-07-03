import os
import importlib
import importlib.machinery
import importlib.util
import sys
import time
from pathlib import Path

def main():
    # Get environment configuration
    datapointmod = os.environ.get('DATAPOINTMOD')
    persistencemod = os.environ.get('PERSISTENCEMOD')
    
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

    # Get the datapoint and write it to the persistence.
    execute(datapoint, persistence)

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
