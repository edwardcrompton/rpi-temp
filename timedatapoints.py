import os
import importlib
import importlib.machinery
import importlib.util
import sys
import time
from pathlib import Path

from datapointinterface import DatapointInterface
from persistenceinterface import PersistenceInterface

def main():
    # Get environment configuration
    datapointclass = os.environ.get('DATAPOINTCLASS') # E.g. datapoint.datapoint
    persistenceclass = os.environ.get('PERSISTENCECLASS')
    
    if datapointclass is None or persistenceclass is None:
        if datapointclass is None:
            print('Please add the DATAPOINTCLASS env var.')
    
        if persistenceclass is None:
            print('Please add the PERSISTENCECLASS env var.')
        
        quit()

    # Load the datapoint class
    datapoint = dynamic_imp(*datapointclass.split('.'))

    # Load the persistence class
    persistence = dynamic_imp(*persistenceclass.split('.'))

    # Get the datapoint and write it to the persistence.
    timedatapoints = TimeDataPoints(datapoint, persistence)
    timedatapoints.execute()

# dynamic import  
def dynamic_imp(name, class_name): 
      
    path = Path(__file__).parent.resolve()

    # find_module() method is used 
    # to find the module and return 
    # its description and path 
    try: 
        spec = importlib.machinery.PathFinder().find_spec(name, [str(path) + "/plugins"])
        mod = importlib.util.module_from_spec(spec)
        sys.modules[name] = mod
        spec.loader.exec_module(mod)   

    except ImportError: 
        print ("module not found: " + name)
          
    try:
        loaded_class = getattr(mod, class_name)
    
    except Exception:
        print ("class not found %s.%s", name, class_name)

    return loaded_class

class TimeDataPoints():
    def __init__(self, datapoint: DatapointInterface, persistence: PersistenceInterface):
        self.datapoint = datapoint
        self.persistence = persistence

    def execute(self):
        current_time = time.localtime()
        formatted_time = time.strftime('%Y-%m-%d %H:%M', current_time)
        self.persistence.write(formatted_time, self.datapoint.get())

# Function Call
if __name__ == '__main__':
    main()
