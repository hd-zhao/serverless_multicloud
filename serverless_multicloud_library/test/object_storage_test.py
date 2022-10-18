
import os
import sys
#print(__file__)
#print(os.path.abspath(__file__))
#print(os.path.dirname(os.path.abspath(__file__)))
#print(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#print(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from src.smlibrary.object_storage import s3
from src.smlibrary.object_storage import gcs
from src.smlibrary.object_storage import oss
from src.smlibrary.object_storage import r2

#AWS S3 test
#s3.upload_file("thumbnail-london","../../credential/aws.json","cat.jpg","../../benchmark_dataset/thumbnail_picture/5mb.jpg")

#Google Storage test
#gcs.upload_file("thumbnail-london","../../credential/google_cloud.json","cat.jpg","../../benchmark_dataset/thumbnail_picture/5mb.jpg")

#Alibaba oss test
#oss.upload_file("thumbnail-london", "/Users/haidongzhao/credential/alibaba.json","cat.jpg", "../../benchmark_dataset/thumbnail_picture/5mb.jpg")
#oss.delete_object("thumbnail-london", "/Users/haidongzhao/credential/alibaba.json","cat.jpg")


# mocked AWS SDKs
#test GCS
from src.smlibrary.object_storage.mocked_s3.to_gcs import to_gcs
#aws_gcs = to_gcs("/Users/haidongzhao/credential/google_cloud.json")
#aws_gcs.upload_file("../../benchmark_dataset/thumbnail_picture/5mb.jpg","thumbnail-london","cat.jpg")
#aws_gcs.delete_object("thumbnail-london", "cat.jpg")
#buf = aws_gcs.get_object("thumbnail-london","cat.jpg")
#aws_gcs.download_file("thumbnail-london", "cat.jpg", "cat.jpg")

# mocked AWS SDKs
#test Alibaba OSS
from src.smlibrary.object_storage.mocked_s3.to_oss import to_oss
#aws_oss = to_oss("/Users/haidongzhao/credential/alibaba.json", "thumbnail-london")
#aws_oss.upload_file("../../benchmark_dataset/thumbnail_picture/5mb.jpg","thumbnail-london","cat.jpg")
#aws_oss.delete_object("thumbnail-london", "cat.jpg")
#buf = aws_oss.get_object("thumbnail-london","cat.jpg")
#aws_oss.download_file("thumbnail-london", "cat.jpg", "cat.jpg")