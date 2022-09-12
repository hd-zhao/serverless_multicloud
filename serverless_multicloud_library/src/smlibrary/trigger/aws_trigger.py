import logging
import boto3
import boto3.session
from botocore.exceptions import ClientError
import json
import os
import io

def invoke(credential,function, event_type,payload,end_point = None):
    aws_credential = json.load(open(credential))
    
    if event_type == 'async':
        invocation_type = 'Event'
    elif event_type == 'sync':
        invocation_type = 'RequestResponse'

    s3_client = boto3.Session().client('lambda',
                              aws_access_key_id = aws_credential["s3"]['Access key ID'],
                              aws_secret_access_key = aws_credential["s3"]['Secret access key'],
                              region_name = "eu-west-2"
                            )
    get_msg = s3_client.invoke(FunctionName=function, 
                     InvocationType=invocation_type,
                     Payload=payload)
    return get_msg