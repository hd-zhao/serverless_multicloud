import uuid
import json
from PIL import Image
from smlibrary.object_storage import s3,r2
from datetime import datetime
import ntp

def resize_image(image_path, resized_path):
    with Image.open(image_path) as image:
        image.thumbnail(tuple(x / 2 for x in image.size))
        image.save(resized_path)



def lambda_handler(event, context):
    record = event['Records'][0]
    bucket = record['s3']['bucket']['name']
    key = record['s3']['object']['key']
    get_time = ntp.get_timestamp_ms()
    if(get_time != 0):
        print("Benchmark object:{} timestamp:{}".format(key, get_time))

    tmpkey = key.replace('/', '')
    download_path = '/tmp/{}{}'.format(uuid.uuid4(), tmpkey)
    upload_path = '/tmp/resize-{}'.format(tmpkey)

    s3.download_file(bucket, "aws.json",key, download_path)
    resize_image(download_path, upload_path)
    r2.upload_file("thumbnailcf", "cloudflare.json", key, upload_path)
    return