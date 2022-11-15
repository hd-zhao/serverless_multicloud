import numpy as np
import onnx
import onnxruntime
import uuid
import json
from smlibrary.object_storage import r2




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

    event = json.loads(request_body)
    bucket = event["bucket"]
    key = event["object"]
    tmpkey = key.replace('/', '')
    download_path = '/tmp/{}{}'.format(uuid.uuid4(), tmpkey)
    r2.download_file(bucket, "cloudflare.json",key, download_path)

    with open(download_path, 'rb') as f:
        img = np.load(f)
    session = onnxruntime.InferenceSession("model.onnx", None)
    input_name = session.get_inputs()[0].name
    output_name = session.get_outputs()[0].name
    data = np.array(img).astype('float32')
    result = session.run([output_name], {input_name: data})
    prediction=int(np.argmax(np.array(result).squeeze(), axis=0))
    print(f"prediction: {prediction}")
    return "%s"%(prediction)