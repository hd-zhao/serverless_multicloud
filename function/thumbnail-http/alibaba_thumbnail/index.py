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
    request_body = environ['wsgi.input'].read(request_body_size)
    evt = json.loads(request_body)
    get_time = ntp.get_timestamp_ms()
    key = evt["upload_id"]
    if(get_time != 0):
        print("Benchmark object:{} timestamp:{}".format(key, get_time))

    return