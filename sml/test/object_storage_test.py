
import os
import sys
#print(__file__)
#print(os.path.abspath(__file__))
#print(os.path.dirname(os.path.abspath(__file__)))
#print(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.object_storage import s3
from src.object_storage import gcs

#AWS S3 test
#s3.upload_file("thumbnail-london","../../credential/aws.json","cat.jpg","../../benchmark_dataset/thumbnail_picture/5mb.jpg")

#Google Cloud test
gcs.upload_file("thumbnail-london","../../credential/google_cloud.json","cat.jpg","../../benchmark_dataset/thumbnail_picture/5mb.jpg")