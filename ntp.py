import requests
from datetime import datetime
import time

def get_timestamp_ms():
    try:
        start_time = time.perf_counter()
        r = requests.get("http://worldtimeapi.org/api/timezone/Europe/London")
        end_time = time.perf_counter()
        element = datetime.strptime(r.json()['utc_datetime'],"%Y-%m-%dT%H:%M:%S.%f+00:00")
        timestamp = datetime.timestamp(element)
        off_set = (end_time-start_time)/2
        return int((timestamp-off_set)*1000)
    except:
        return 0
