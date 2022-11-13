from smlibrary.object_storage import r2
import os 
credential = os.path.expanduser("~/credential/cloudflare.json")
print(credential)
while True:
    r2.empty_bucket("thumbnailcf", credential)