import fc2
import os
import io
import logging
import json
import requests

#global name
service_name = "service1"

def invoke(credential,function, event_type,Payload,end_point = None):
        ali_credential = json.load(open(credential))
        fc_client = fc2.Client(
                endpoint = end_point,
                accessKeyID = ali_credential['oss']['Access key ID'],
                accessKeySecret = ali_credential['oss']['Secret access key']
        )


        if event_type == 'async':
                response = fc_client.invoke_function(serviceName=service_name, functionName=function,payload=Payload, headers = {'x-fc-invocation-type': 'Async'})
                return response
        elif event_type == 'sync':
                response = fc_client.invoke_function(serviceName=service_name, functionName=function,payload=Payload)
                return response
        else:
                print("please input sync or asyc")
                exit()

def container_inovke(credential,function,event_type,Payload):
        ali_credential = json.load(open(credential))
        url=ali_credential['end_point'][function]
        response = requests.post(
                            url, 
                            #headers={'Authorization': f"Bearer storage-service@amiable-bridge-342803.iam.gserviceaccount.com", "Content-Type": "application/json"},
                            headers={"x-fc-invocation-target":"2016-08-15/proxy/PythonFlaskCustomContainer/python-flask"},
                            data=Payload
                        )
        return response



