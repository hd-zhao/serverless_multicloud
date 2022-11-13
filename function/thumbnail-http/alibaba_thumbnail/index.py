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



def handler(environ, start_response):
    context = environ['fc.context']
    request_uri = environ['fc.request_uri']
    for k, v in environ.items():
        if k.startswith("HTTP_"):
            # process custom request headers
            pass

    # get request_body
    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
    except (ValueError):
        request_body_size = 0
    request_body = environ['wsgi.input'].read(request_body_size)

    # get request_method
    request_method = environ['REQUEST_METHOD']

    # get path info
    path_info = environ['PATH_INFO']

    # get server_protocol
    server_protocol = environ['SERVER_PROTOCOL']

    # get content_type
    try:
        content_type = environ['CONTENT_TYPE']
    except (KeyError):
        content_type = " "

    # get query_string
    try:
        query_string = environ['QUERY_STRING']
    except (KeyError):
        query_string = " "

    evt = json.loads(request_body)
    get_time = ntp.get_timestamp_ms()
    key = evt["upload_id"]
    if(get_time != 0):
        print("Benchmark object:{} timestamp:{}".format(key, get_time))

    return "hello"