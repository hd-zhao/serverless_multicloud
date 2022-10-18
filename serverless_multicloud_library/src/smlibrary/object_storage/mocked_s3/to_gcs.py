import logging
import os
import io
from google.cloud import storage

class to_gcs:
    def __init__(self, credential):
        self.storage_client = storage.Client.from_service_account_json(credential)

    def upload_file(self, local_object_path, bucket, bucket_object_path):  #upload object
        
        if bucket_object_path is None:
            bucket_object_path = os.path.basename(local_object_path)
        try:
            self.storage_client.bucket(bucket).blob(bucket_object_path).upload_from_filename(local_object_path)
        except Exception as e:
            logging.error(e)
            return False


    def download_file(self, bucket, bucket_object_path, local_object_path):   #download_object
        if local_object_path is None:
            local_object_path = os.path.basename(bucket_object_path)
        try:
            self.storage_client.bucket(bucket).blob(bucket_object_path).download_to_filename(local_object_path)
        except Exception as e:
            logging.error(e)
            return False


    def get_object(self, bucket, bucket_object_path):
        try:
            buf = self.storage_client.bucket(bucket).blob(bucket_object_path).download_as_bytes()
            return buf
        except Exception as e:
            logging.error(e)
            return False

    def put_object(self, local_object_path, bucket, bucket_object_path):
        try:
            self.storage_client.bucket(bucket).blob(bucket_object_path).upload_from_string(local_object_path)
        except Exception as e:
            logging.error(e)
            return False
    
    def delete_object(self, bucket, bucket_object_path):
        try:
            self.storage_client.bucket(bucket).blob(bucket_object_path).delete()
        except Exception as e:
            logging.error(e)
            return False
