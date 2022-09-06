import fc2
import os
import io
import logging
import json
import requests

#global name
service_name = "service1"
bytes('hello_world'.encode('utf-8'))
def invoke(credential,function, event_type,Payload):
        ali_credential = json.load(open(credential))
        fc_client = fc2.Client(
                endpoint=ali_credential['end_point'][function],
                accessKeyID=ali_credential['Access key ID'],
                accessKeySecret=ali_credential['Secret access key']
                )

        #path='/2016-08-15/proxy/service1/function3'
        #req = fc_client.do_http_request('POST', service_name, function, path,body='hello')
        #print(req)
        if event_type == 'async':
                fc_client.invoke_function(serviceName=service_name, functionName=function,payload=Payload, headers = {'x-fc-invocation-type': 'Async'})
        elif event_type == 'sync':
                fc_client.invoke_function(serviceName=service_name, functionName=function,payload=Payload)
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



