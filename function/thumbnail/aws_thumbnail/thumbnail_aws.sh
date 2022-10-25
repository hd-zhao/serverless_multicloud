mkdir package
cp -r lambda_function.py ./package
cp -r ../../../ntp.py ./package
cp -r ~/credential/aws.json ./package
cp -r ~/credential/cloudflare.json ./package
pip install --target ./package -r requirements.txt
cd package && zip -r aws_thumbnail.zip  . && cd ..
mv package/aws_thumbnail.zip ./
rm -rf package