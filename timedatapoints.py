import os
import importlib
import time

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
    datapoint = class_import(datapointclass)

    # Load the persistence class
    persistence = class_import(persistenceclass)

    # 
    timedatapoints = TimeDataPoints(datapoint, persistence)
    timedatapoints.execute()

def class_import(name):
    components = name.split('.')
    mod = __import__(components[0])
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod

class TimeDataPoints():
    def __init__(self, datapoint: DatapointInterface, persistence: PersistenceInterface):
        self.datapoint = datapoint
        self.persistence = persistence

    def execute(self):
        self.persistence.write(time.time(), self.datapoint.get())    

# Function Call
if __name__ == '__main__':
    main()