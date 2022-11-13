from datetime import datetime
import uuid
import time
import json
import csv
import os
from threading import Thread
from smlibrary.trigger import aws_trigger, google_trigger, alibaba_trigger
import random

def add_payload(dict,unique_id):
    dict["upload_id"]=unique_id
    return dict

def invoke(provider, output, latency_class, credential, function, payload, unique_id):
    operation_time_start = time.perf_counter()
    if(provider == "aws"):
        aws_trigger.invoke(credential,function,"sync",payload)
    elif(provider == "google"):
        # now function = end_point, configured in credential file
        return_value = google_trigger.invoke(credential,function,"sync",payload, function)
    elif(provider == "alibaba"):
        # add endpoint, configured in credential file
        return_value = alibaba_trigger.invoke(credential,function,"sync",payload, function)
        print(return_value.headers['content-length'])
    else:
        print("Please check provider.")
        exit()

    operation_duration = time.perf_counter() - operation_time_start
    if(latency_class == "response_time"):
        output.writerow([int(operation_duration), unique_id])


def operation(provider, credential, function, payload, application, poisson_rate, memory_allocation, latency_class, duration):

    # save local logs to thr cloud log query directory for collective analysis
    output = csv.writer(open('../logging_query/log/'+provider+'-'+application+'-'+memory_allocation+".csv", 'w'))
    if(latency_class == "e2e_delay"):
        output.writerow(['timestamp', 'object'])
    elif(latency_class == "response_time"):
        output.writerow(['latency', 'object'])
    
    start_time = time.perf_counter()
    while(time.perf_counter() - start_time <= duration * 60):   #benchmark duration
        #add unique id to an object
        unique_id = str(uuid.uuid4())
        new_payload = json.dumps(add_payload(payload, unique_id))
        
        if(latency_class == "e2e_delay"):
            output.writerow([int(datetime.timestamp(datetime.now())*1000), unique_id])
        

        Thread(target=invoke, args=(provider, output, latency_class, credential, function, new_payload, unique_id)).start()
        time.sleep(random.expovariate(poisson_rate))

        print(f"time elapsed: {time.perf_counter() - start_time}")