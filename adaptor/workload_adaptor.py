from smlibrary.object_storage import gcs,oss,s3,r2
from smlibrary.trigger import aws_trigger,alibaba_trigger,google_trigger
from datetime import datetime
from threading import Thread
from numpy.random import choice
import uuid
import time
import json
import argparse
import csv
import os

concurrent_request_number = 20

def add_payload(dict,unique_id):
    dict["upload_id"]=unique_id
    return dict

def exec_aws_thumbnail(bucket,credential,object_name,picture_location):
    aws_s3.upload_file(bucket,credential,object_name,picture_location)

def exec_google_thumbnail(bucket,credential,object_name,picture_location):
    gc_storage.upload_file(bucket,credential,object_name,picture_location)

def exec_ali_thumbnail(bucket,credential,object_name,picture_location):
    ali_object.upload_file(bucket,credential,object_name,picture_location)

def exec_aws_http(credential,function,invocation_type,payload):
    aws_trigger.invoke(credential,function,invocation_type,payload)

def exec_ali_http(credential,function,invocation_type,payload):
    ali_trigger.invoke(credential,function,invocation_type,payload)

def exec_ali_container(credential,function,invocation_type,payload):
    ali_trigger.container_inovke(credential,function,invocation_type,payload)

def exec_google_http(credential,function,invocation_type,payload):
    google_trigger.invoke(credential,function,invocation_type,payload)


def thumbnail_exec(provider,bucket,credential,picture_location,picture_size):
    #logging to local
    print(provider,bucket,credential,picture_location,picture_size)
    output = csv.writer(open('./logging_query/logging-'+provider+'-'+picture_size+".csv", 'w'))
    output.writerow(['timestamp', 'object'])

    
    for i in range(0,30):
        start_time = time.perf_counter()
        threads = []
        if provider != "multicloud":
            for i in range(0,concurrent_request_number):
                unique_id = str(uuid.uuid4())
                object_name = unique_id+".jpg"
                timestamp_ms = int(datetime.timestamp(datetime.now())*1000)
                output.writerow([timestamp_ms, object_name])
                if provider == 'aws':
                    t = Thread(target=exec_aws_thumbnail, args=(bucket,credential,object_name,picture_location))  
                if provider == 'google':
                    t = Thread(target=exec_google_thumbnail, args=(bucket,credential,object_name,picture_location))
                if provider == 'ali':
                    t = Thread(target=exec_ali_thumbnail, args=(bucket,credential,object_name,picture_location))

                threads.append(t)   
        else:
            #multicloud shedule: random choose provider alibaba or google
            for i in range(0,concurrent_request_number):
                unique_id = str(uuid.uuid4())
                object_name = unique_id+".jpg"
                random_provider = choice(multicloud_choice,p=[0.16,0.84,0]) 
                config = json.load(open("./benchmark_conf/thumbnail.json"))
                timestamp_ms = int(datetime.timestamp(datetime.now())*1000)
                output.writerow([timestamp_ms, object_name])
                if random_provider == 'ali':
                    t = Thread(target=exec_ali_thumbnail, args=(config[random_provider][picture_size]['bucket'],\
                                config[random_provider]["credential"],\
                                object_name,\
                                config[random_provider][picture_size]['picture']))
                if random_provider == 'aws':
                    t = Thread(target=exec_aws_thumbnail, args=(config[random_provider][picture_size]['bucket'],\
                                config[random_provider]["credential"],\
                                object_name,\
                                config[random_provider][picture_size]['picture']))
                
                threads.append(t)
             
        for t in threads:
            t.start()
        
        for t in threads:
            t.join()

        end_time = time.perf_counter()
        interval_time = end_time - start_time
        burst_frequency = 30
        if(interval_time < burst_frequency):
            time.sleep(burst_frequency-interval_time)
        end_time = time.perf_counter() - start_time
        print(f'It took {interval_time: 0.2f} and {end_time: 0.2f} second(s) to complete transmission and finish.')


def http_exec(provider,invoke_num,app):
    print(provider,invoke_num)
    json_file_name = "./benchmark_conf/"+app+".json"
    trigger_config = json.load(open(json_file_name))
    if provider != "multicloud":
        function = trigger_config[invoke_num][provider]["function"]
        payload = trigger_config[invoke_num][provider]["payload"]

    else:
        function_aws = trigger_config[invoke_num][provider]["aws"]["function"]
        payload_aws = trigger_config[invoke_num][provider]["aws"]["payload"]
        function_google = trigger_config[invoke_num][provider]["google"]["function"]
        payload_google = trigger_config[invoke_num][provider]["google"]["payload"]
        print("aws:{} function:{}".format(function_aws,payload_aws))
        print("google:{} function:{}".format(function_google,payload_google))


    output = csv.writer(open('./logging_query/logging-'+provider+"-"+app+"-"+invoke_num+".csv", 'w'))
    output.writerow(['timestamp', 'object'])
    for i in range(0,12):
        start_time = time.perf_counter()
        threads = []
        if provider != "multicloud":
            for i in range(0,concurrent_request_number):
                unique_id = str(uuid.uuid4())
       
                if app == 'normalization':
                    object_name = unique_id+".jpg"
                else:
                    object_name = unique_id
                new_payload = json.dumps(add_payload(payload,object_name))
                
  
                
                #print(object_name,str(int(datetime.timestamp(datetime.utcnow())*1000)))
                #google_trigger.invoke(trigger_config["google_credential"],function,"sync",new_payload)
                #ali_trigger.invoke(trigger_config["ali_credential"],function,"sync",new_payload)
                #aws_trigger.invoke(trigger_config["aws_credential"],function,"sync",new_payload)
                #exit()
                if app == "normalization" or 'mltraining':
                    if provider == 'aws':
                        t = Thread(target=exec_aws_http, args=(trigger_config["aws_credential"],function,"sync",new_payload)) 
                    if provider == 'google':
                        t = Thread(target=exec_google_http, args=(trigger_config["google_credential"],function,"sync",new_payload)) #google only priovide "sync" invocation
                    if provider == 'ali':
                        print(new_payload)
                        if app == 'mltraining':
                            t = Thread(target=exec_ali_container, args=(trigger_config["ali_credential"],function,"sync",new_payload))
                        else:
                            t = Thread(target=exec_ali_http, args=(trigger_config["ali_credential"],function,"sync",new_payload))
                else:
                    print("no this app")
                    exit()
                
                    
                timestamp_ms = int(datetime.timestamp(datetime.now())*1000)
                output.writerow([timestamp_ms, object_name])
                threads.append(t)
        if provider == "multicloud":
    
            for i in range(0,concurrent_request_number):
                unique_id = str(uuid.uuid4())
                object_name = unique_id+".jpg"
                #random_provider = random.choice(multicloud_choice) 

        for t in threads:
            t.start()
        
        for t in threads:
            t.join()
        end_time = time.perf_counter()
        interval_time = end_time - start_time
        burst_frequency = 0
        if(interval_time<burst_frequency):
            time.sleep(burst_frequency-interval_time)
        end_time = time.perf_counter() - start_time
        print(f'It took {interval_time: 0.2f} and {end_time: 0.2f} second(s) to complete transmission and finish.')

        


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--provider", dest="provider", default= None,
                        help="benchmark provider")
    
    parser.add_argument("-m", "--mb", dest="mb", default=None,
                        help="thumbnail picture")
    
    parser.add_argument("-n", "--normalization_invoke", dest="nor", default=None,
                        help="normalization, please direct input the invoke number, configured in json file")
    parser.add_argument("-t", "--ml_training_invoke", dest="mlt", default=None,
                        help="ml training, please direct input the invoke number, configured in json file")
    args = parser.parse_args()

    if args.provider == None:
        print("please input the provider")
        exit()
    
    if args.nor != None:
        print("normalization benchmarking!")
        if args.provider == "multicloud":
            print("hello")
        else:
            http_exec(args.provider,args.nor,"normalization")

    if args.mlt != None:
        print("ml training benchmarking!")
        if args.provider == "multicloud":
            print("hello")
        else:
            http_exec(args.provider,args.mlt,"mltraining")


    if args.mb != None:
        print("thumbnail benchmarking!")
        config = json.load(open("./benchmark_conf/thumbnail.json"))
        picture_size = args.mb
        if args.provider == "multicloud":
            thumbnail_exec("multicloud","bucket","credential","picture",picture_size)
        else:
            thumbnail_exec(args.provider,config[args.provider][picture_size]['bucket'],config[args.provider]["credential"],config[args.provider][picture_size]['picture'],picture_size)

    

