from smlibrary.object_storage import gcs,oss,s3,r2
from datetime import datetime
from threading import Thread
from numpy.random import choice
import uuid
import time
import json
import argparse
import csv
import os

def add_payload(dict,unique_id):
    dict["upload_id"]=unique_id
    return dict

def update_operation(provider,credential,bucket,object,application):
    #logging to local
    print(provider,bucket,credential,object)
    output = csv.writer(open('../logging_query/'+provider+'/logging-'+provider+'-'+application+".csv", 'w'))
    output.writerow(['timestamp', 'object'])
    
