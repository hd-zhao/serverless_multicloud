import uuid
import json
from PIL import Image
from datetime import datetime
from smlibrary.object_storage import oss,r2
import ntp

def resize_image(image_path, resized_path):
    with Image.open(image_path) as image:
        image.thumbnail(tuple(x / 2 for x in image.size))
        image.save(resized_path)



def handler(event, context):
    evt = json.loads(event)
    bucket = evt['events'][0]['oss']['bucket']['name']
    key = evt['events'][0]['oss']['object']['key']

    get_time = ntp.get_timestamp_ms()
    if(get_time != 0):
        print("Benchmark object:{} timestamp:{}".format(key, get_time))

    tmpkey = key.replace('/', '')
    download_path = '/tmp/{}{}'.format(uuid.uuid4(), tmpkey)
    upload_path = '/tmp/resize-{}'.format(tmpkey)

    oss.download_file(bucket, "alibaba.json",key, download_path)

    resize_image(download_path, upload_path)
    
    r2.upload_file("thumbnailcf", "cloudflare.json", key, upload_path)
    return
