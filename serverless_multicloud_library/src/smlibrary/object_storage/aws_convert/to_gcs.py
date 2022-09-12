import sys
import os
from .. import gcs

def upload_file(local_object_path, bucket, bucket_object_path,credential):  #upload object
    gcs.upload_file(bucket,credential,bucket_object_path,local_object_path)


def download_file(bucket, bucket_object_path, local_object_path,credential):   #download_object
    gcs.download_file(bucket,credential,bucket_object_path,local_object_path)


def get_object(bucket, bucket_object_path,credential):
    buf = gcs.get_object(bucket, credential, bucket_object_path)
    return buf

def put_object(local_object_path, bucket, bucket_object_path,credential):
    gcs.upload_fileobj(bucket,credential,bucket_object_path,local_object_path)
    
