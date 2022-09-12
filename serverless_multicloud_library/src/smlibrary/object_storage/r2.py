import logging
import boto3
import boto3.session
from botocore.exceptions import ClientError
import json
import os
import io

def input_credential(credential):
    cloudflare_credential = json.load(open(credential))
    
    s3_client = boto3.client('s3',
                            endpoint_url = 'https://'+cloudflare_credential["r2"]['Account ID']+'.r2.cloudflarestorage.com',  
                            aws_access_key_id = cloudflare_credential["r2"]['Access key ID'],
                            aws_secret_access_key = cloudflare_credential["r2"]['Secret access key'],
                            region_name = "auto"
                            )
    return s3_client

def upload_file(bucket, credential, bucket_object_path=None, local_object_path=None):
    s3_client = input_credential(credential)
    if bucket_object_path is None:
        bucket_object_path = os.path.basename(local_object_path)
    try:
        response = s3_client.upload_file(local_object_path, bucket, bucket_object_path)
    except ClientError as e:
        logging.error(e)
        return False

def upload_fileobj(bucket, credential, bucket_object_path=None, local_object_path=None): #upload_from_mem
    s3_client = input_credential(credential)
    try:
        response = s3_client.upload_fileobj(local_object_path, bucket, bucket_object_path)
    except ClientError as e:
        logging.error(e)
        return False

def download_file(bucket, credential, bucket_object_path=None, local_object_path=None): #download_object
    s3_client = input_credential(credential)
    try:
        response = s3_client.download_file(bucket, bucket_object_path, local_object_path)
    except ClientError as e:
        logging.error(e)
        return False

def download_fileobj(bucket, credential, bucket_object_path=None, local_object_path=None): #download_to_mem
    s3_client = input_credential(credential)
    try:
        buf = io.BytesIO()
        response = s3_client.download_fileobj(bucket, bucket_object_path, buf)
        buf.seek(0)
        filecontent_bytes = buf.getvalue() # Get file content as bytes
        return buf
    except ClientError as e:
        logging.error(e)
        return False

def delete_object(bucket, credential, bucket_object_path=None, local_object_path=None):#delete_object
    s3_client = input_credential(credential)
    try:
        response = s3_client.delete_object(Bucket=bucket, Key=bucket_object_path)
    except ClientError as e:
        logging.error(e)
        return False
def get_object(bucket, credential, bucket_object_path=None, local_object_path=None):
    s3_client = input_credential(credential)
    try:
        response = s3_client.get_object(Bucket=bucket, Key=bucket_object_path)
        return response
    except ClientError as e:
        logging.error(e)
        return False

def put_object(bucket, credential, bucket_object_path=None, local_object_path=None):
    s3_client = input_credential(credential)
    try:
        response = s3_client.put_object(Body=local_object_path, Bucket=bucket, Key=bucket_object_path)
        return response
    except ClientError as e:
        logging.error(e)
        return False
        
def empty_bucket(bucket,credential):
    
    s3_client = input_credential(credential)
    bucketListResultSet = s3_client.list_objects(Bucket=bucket)
    
    for i in bucketListResultSet['Contents']:
        s3_client.delete_object(Bucket=bucket, Key=i['Key'])


