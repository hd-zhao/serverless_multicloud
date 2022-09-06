import logging
import os
import io
from google.cloud import storage

def upload_file(bucket, credential, bucket_object_path=None, local_object_path=None): #upload object
    storage_client = storage.Client.from_service_account_json(credential)
    if bucket_object_path is None:
        bucket_object_path = os.path.basename(local_object_path)
    try:
        storage_client.bucket(bucket).blob(bucket_object_path).upload_from_filename(local_object_path)
    except Exception as e:
        logging.error(e)
        return False

def upload_fileobj(bucket, credential, bucket_object_path=None, local_object_path=None): #upload_from_mem
    storage_client = storage.Client.from_service_account_json(credential)
    try:
        storage_client.bucket(bucket).blob(bucket_object_path).upload_from_string(local_object_path)
    except Exception as e:
        logging.error(e)
        return False
    
def download_file(bucket, credential, bucket_object_path=None, local_object_path=None): #download_object
    storage_client = storage.Client.from_service_account_json(credential)
    if local_object_path is None:
        local_object_path = os.path.basename(bucket_object_path)
    try:
        storage_client.bucket(bucket).blob(bucket_object_path).download_to_filename(local_object_path)
    except Exception as e:
        logging.error(e)
        return False

def get_object(bucket, credential, bucket_object_path=None, local_object_path=None): #download_to_mem
    storage_client = storage.Client.from_service_account_json(credential)
    try:
        #buf = io.BytesIO()
        buf=storage_client.bucket(bucket).blob(bucket_object_path).download_as_bytes()
        #buf.seek(0)
        return buf
    except Exception as e:
        logging.error(e)
        return False

def delete_object(bucket, credential, bucket_object_path=None, local_object_path=None):#delete_object
    storage_client = storage.Client.from_service_account_json(credential)
    try:
        storage_client.bucket(bucket).blob(bucket_object_path).delete()
    except Exception as e:
        logging.error(e)
        return False