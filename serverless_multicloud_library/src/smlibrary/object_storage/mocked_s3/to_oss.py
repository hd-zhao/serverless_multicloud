import json
import os
import io
import logging
import oss2

class to_oss:
    def __init__(self, credential, bucket):
        ali_credential = json.load(open(credential))
        auth = oss2.Auth(ali_credential['oss']['Access key ID'], ali_credential['oss']['Secret access key'])
        self.ali_bucket = oss2.Bucket(auth, ali_credential['oss']['alibaba_endpoint'], bucket, enable_crc=False)


    def upload_file(self, local_object_path, bucket, bucket_object_path):  #upload object
        if bucket_object_path is None:
            bucket_object_path = os.path.basename(local_object_path)
        try:
            self.ali_bucket.put_object_from_file(bucket_object_path, local_object_path)
        except Exception as e:
            logging.error(e)
            return False


    def download_file(self, bucket, bucket_object_path, local_object_path):   #download_object
        try:
            self.ali_bucket.get_object_to_file(bucket_object_path, local_object_path)
        except Exception as e:
            logging.error(e)
        return False


    def get_object(self, bucket, bucket_object_path):
        try:
            buf = self.ali_bucket.get_object(bucket_object_path).read()
            return buf # Get file content as bytes
        except Exception as e:
            logging.error(e)
        return False

    def put_object(self, local_object_path, bucket, bucket_object_path):
        try:
            self.ali_bucket.put_object(bucket_object_path, local_object_path)
        except Exception as e:
            logging.error(e)
        return False
    
    def delete_object(self, bucket, bucket_object_path):
        try:
            self.ali_bucket.delete_object(bucket_object_path)
        except Exception as e:
            logging.error(e)
        return False