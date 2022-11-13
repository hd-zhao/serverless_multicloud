mkdir package
cp -r index.py ./package
cp -r ../../../ntp.py ./package
cp -r ~/credential/alibaba.json ./package
cp -r ~/credential/cloudflare.json ./package
cp -r  requirements.txt ./package
cd package && zip -r alibaba_thumbnail.zip  . && cd ..
mv package/alibaba_thumbnail.zip ./
rm -rf package