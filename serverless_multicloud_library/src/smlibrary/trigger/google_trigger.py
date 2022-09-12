
import requests
import json
import os
import io
import logging


def invoke(credential,function, event_type,payload, end_point = None):
    google_credential = json.load(open(credential))
    if end_point == None:
        print("Please input the url of funciton")
        return 0
    url = end_point

    response = requests.post(
                            url, 
                            #headers={'Authorization': f"Bearer storage-service@amiable-bridge-342803.iam.gserviceaccount.com", "Content-Type": "application/json"},
                            headers={"Content-Type": "application/json"},
                            data=payload
                        )
    return response