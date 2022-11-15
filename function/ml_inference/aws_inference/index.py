
import numpy as np
import onnx
import onnxruntime
import uuid
from smlibrary.object_storage import r2


def handler(event, context):

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
    print("success")
    return "%s"%(prediction)