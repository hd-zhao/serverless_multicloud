from datetime import datetime
import uuid
import time
import json
import csv
import os
from threading import Thread
from smlibrary.object_storage import s3, gcs, oss
import random

def upload_thread(provider,output, latency_class, bucket, credential, object_name, object):
    operation_time_start = time.perf_counter()
    if(provider == "aws"):
        s3.upload_file(bucket, credential, object_name, object)
    elif(provider == "google"):
        gcs.upload_file(bucket, credential, object_name, object)
    elif(provider == "alibaba"):
        oss.upload_file(bucket, credential, object_name, object)
    else:
        print("Please check provider.")
        exit()
    operation_time_end = time.perf_counter()
    operation_duration = operation_time_end - operation_time_start
    if(latency_class == "response_time"):
        output.writerow([int(operation_duration), object_name])



def operation(provider, credential, bucket, object, application, poisson_rate, memory_allocation, latency_class, duration):

    # save local logs to thr cloud log query directory for collective analysis

    if(latency_class == "e2e_delay"):
        output = csv.writer(open('../logging_query/log/'+provider+'-'+application+'-'+memory_allocation+".csv", 'w'))
        output.writerow(['timestamp', 'object'])
    elif(latency_class == "response_time"):
        output = csv.writer(open('../dataset/'+provider+'-'+application+'-'+memory_allocation+"-latency.csv", 'w'))
        output.writerow(['latency', 'object'])
    
    start_time = time.perf_counter()
    while(time.perf_counter() - start_time <= duration * 60):   #benchmark duration
        #add unique id to an object
        unique_id = str(uuid.uuid4())
        object_name = unique_id + os.path.splitext(object)[-1]

        
        if(latency_class == "e2e_delay"):
            output.writerow([int(datetime.timestamp(datetime.now())*1000), object_name])
        
        if(operation == "upload"):
            Thread(target=upload_thread, args=(provider, output, latency_class, bucket, credential, object_name, object)).start()
        time.sleep(random.expovariate(poisson_rate))

        print(f"time elapsed: {time.perf_counter() - start_time}")



    
