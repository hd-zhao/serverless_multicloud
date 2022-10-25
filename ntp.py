import ntplib
#from datetime import datetime
import time

def get_timestamp_ms():
    try:
        c = ntplib.NTPClient()
        start_time = time.perf_counter()
        response = c.request('uk.pool.ntp.org', version=3).tx_time
        #r = requests.get("http://worldtimeapi.org/api/timezone/Europe/London")
        end_time = time.perf_counter()
        #element = datetime.strptime(r.json()['utc_datetime'],"%Y-%m-%dT%H:%M:%S.%f+00:00")
        #timestamp = datetime.timestamp(element)
        timestamp = int(response*1000)
        off_set = (end_time-start_time)/2
        return int((timestamp-off_set*1000))
    except:
        return 0

