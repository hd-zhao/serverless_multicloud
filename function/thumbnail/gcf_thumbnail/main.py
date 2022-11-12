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


def make_thumbnail(data, context):
    # Get the image from GCS
    bucket = data['bucket']
    keys = data['name']
    get_time = ntp.get_timestamp_ms()
    if(get_time != 0):
        print("Benchmark object {} timestamp {}".format(keys, get_time))

    tmpkey = keys.replace('/', '')
    download_path = '/tmp/{}{}'.format(uuid.uuid4(), tmpkey)
    upload_path = '/tmp/resize-{}'.format(tmpkey)
    gcs.download_file(bucket, "google_cloud.json",keys,download_path)

    # Create a new image object and resample it
    resize_image(download_path, upload_path)

    # Upload the resampled file to the cloudflare bucket
    r2.upload_file("thumbnailcf", "cloudflare.json", keys, upload_path)
    return