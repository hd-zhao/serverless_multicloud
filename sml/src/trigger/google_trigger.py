
import requests
import json
import os
import io
import logging


def invoke(credential,function, event_type,payload):
    google_credential = json.load(open(credential))
    url = google_credential["end_point"][function]
    #data = payload
    #print("{} {}".format(url,data))
    response = requests.post(
                            url, 
                            #headers={'Authorization': f"Bearer storage-service@amiable-bridge-342803.iam.gserviceaccount.com", "Content-Type": "application/json"},
                            headers={"Content-Type": "application/json"},
                            data=payload
                        )
    return response