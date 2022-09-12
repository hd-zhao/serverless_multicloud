import json
import os
import io
import logging
import oss2

def input_credential(credential, bucket):
    ali_credential = json.load(open(credential))
    
    auth = oss2.Auth(ali_credential['oss']['Access key ID'], ali_credential['oss']['Secret access key'])
    bucket = oss2.Bucket(auth, 'http://oss-eu-west-1.aliyuncs.com', bucket, enable_crc=False)
    return bucket

def upload_file(bucket, credential, bucket_object_path=None, local_object_path=None):
    ali_bucket = input_credential(credential,bucket)
    if bucket_object_path is None:
        bucket_object_path = os.path.basename(local_object_path)
    try:
        ali_bucket.put_object_from_file(bucket_object_path, local_object_path)
    except Exception as e:
        logging.error(e)
        return False

def download_file(bucket, credential, bucket_object_path=None, local_object_path=None): #download_object
    ali_bucket = input_credential(credential,bucket)
    try:
        ali_bucket.get_object_to_file(bucket_object_path, local_object_path)
    except Exception as e:
        logging.error(e)
        return False



def get_object(bucket, credential, bucket_object_path=None, local_object_path=None):
    ali_bucket = input_credential(credential,bucket)
    try:
        buf = ali_bucket.get_object(bucket_object_path)
        return buf # Get file content as bytes
    except Exception as e:
        logging.error(e)
        return False

def put_object(bucket, credential, bucket_object_path=None, local_object_path=None):
    ali_bucket = input_credential(credential,bucket)
    try:
        ali_bucket.put_object(bucket_object_path, local_object_path)

    except Exception as e:
        logging.error(e)
        return False
