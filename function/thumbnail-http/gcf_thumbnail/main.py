from PIL import Image
import uuid
import os
import sys
from datetime import datetime
from smlibrary.object_storage import gcs,r2
import ntp

def resize_image(image_path, resized_path):
  with Image.open(image_path) as image:
      image.thumbnail(tuple(x / 2 for x in image.size))
      image.save(resized_path)


def make_thumbnail(request):
    # Get the image from GCS
    event = request.get_json()
    keys = event["upload_id"]
    get_time = ntp.get_timestamp_ms()
    if(get_time != 0):
        print("Benchmark object {} timestamp {}".format(keys, get_time))

    return "OK"