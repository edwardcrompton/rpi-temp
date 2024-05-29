from datapointinterface import DatapointInterface

class Temperature(DatapointInterface):
    def get():

        # Read Temperature
        tempread=`cat /sys/bus/w1/devices/10-000802b4ba0e/w1_slave`
        # Format
        temp=`echo "scale=2; "\`echo ${tempread##*=}\`" / 1000" | bc`

        # Output
        return temp