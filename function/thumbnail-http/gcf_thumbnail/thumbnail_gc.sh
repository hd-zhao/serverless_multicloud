mkdir package
cp -r main.py ./package
cp -r ../../../ntp.py ./package
cp -r ~/credential/google_cloud.json ./package
cp -r ~/credential/cloudflare.json ./package
cp -r requirements.txt ./package
cd package && zip -r gc_thumbnail.zip  . && cd ..
mv package/gc_thumbnail.zip ./
rm -rf package