from datapointinterface import DatapointInterface
import subprocess
import re
from pathlib import Path

# To set up create a symlink from the 1-wire device file to thermometer:
# ln -s /sys/devices/w1_bus_master1/28-00000f1a29fc/w1_slave thermometer

class Temperature(DatapointInterface):
    def get():

        path = Path(__file__).parent.resolve()

        # Read Temperature
        tempread = subprocess.getoutput('cat ' + str(path) + '/thermometer')
        # Format
        #temp = subprocess.getoutput('echo "scale=2; "\`echo ${tempread##*=}\`" / 1000" | bc')
        temp = re.search('t=([0-9]*)', tempread)

        # Output
        return temp[1]
