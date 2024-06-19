from redis import Redis
from rq import Queue
from rq import Retry

def process(timestamp, datapoint):
    try:
        with open('/tmp/data.out', 'a') as the_file:
            the_file.write(str(timestamp) + '\t' + str(datapoint) + '\n')
    except Exception as e: print(e)
    return

def write(timestamp, datapoint):
    q = Queue(connection=Redis())
    result = q.enqueue(process, timestamp, datapoint, retry=Retry(max=3, interval=[60, 600, 3600]))
