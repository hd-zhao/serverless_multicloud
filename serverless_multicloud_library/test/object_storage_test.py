
import os
import sys
#print(__file__)
#print(os.path.abspath(__file__))
#print(os.path.dirname(os.path.abspath(__file__)))
#print(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.smlibrary.object_storage import s3
from src.smlibrary.object_storage import gcs
from src.smlibrary.object_storage import oss
from src.smlibrary.object_storage import r2

#AWS S3 test
#s3.upload_file("thumbnail-london","../../credential/aws.json","cat.jpg","../../benchmark_dataset/thumbnail_picture/5mb.jpg")

#Google Cloud test
#gcs.upload_file("thumbnail-london","../../credential/google_cloud.json","cat.jpg","../../benchmark_dataset/thumbnail_picture/5mb.jpg")

#Alibaba 

#cloudflare
#r2.upload_file("thumbnailcf","../../credential/cloudflare.json","cat.jpg","../../benchmark_dataset/thumbnail_picture/5mb.jpg")

from src.smlibrary.object_storage.aws_convert import to_gcs
from src.smlibrary.object_storage.aws_convert import to_oss
#to_gcs.upload_file("../../benchmark_dataset/thumbnail_picture/5mb.jpg","thumbnail-london","cat.jpg","../../credential/google_cloud.json")
#buf = to_gcs.get_object("thumbnail-london","cat.jpg","../../credential/google_cloud.json")

to_oss.upload_file("../../benchmark_dataset/thumbnail_picture/5mb.jpg","normali","cat.jpg","../../credential/alibaba.json")
