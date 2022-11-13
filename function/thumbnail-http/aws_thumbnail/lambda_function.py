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
    key = event["upload_id"]
    get_time = ntp.get_timestamp_ms()
    if(get_time != 0):
        print("Benchmark object:{} timestamp:{}".format(key, get_time))
    return
