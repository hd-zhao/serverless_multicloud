import sys
import os
from .. import oss

def upload_file(local_object_path, bucket, bucket_object_path,credential):  #upload object
    oss.upload_file(bucket,credential,bucket_object_path,local_object_path)


def download_file(bucket, bucket_object_path, local_object_path,credential):   #download_object
    oss.download_file(bucket,credential,bucket_object_path,local_object_path)

def get_object(bucket, bucket_object_path,credential):
    buf = oss.get_object(bucket, credential, bucket_object_path)
    return buf

def put_object(local_object_path, bucket, bucket_object_path,credential):
    oss.upload_fileobj(bucket,credential,bucket_object_path,local_object_path)
    
