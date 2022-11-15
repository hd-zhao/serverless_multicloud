mkdir package
cp -r main.py ./package
cp -r ~/credential/cloudflare.json ./package
cp -r ../model.onnx ./package
cp -r requirements.txt ./package
cd package && zip -r google_inference.zip  . && cd ..
mv package/google_inference.zip ./
rm -rf package