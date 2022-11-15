mkdir package
cp -r index.py ./package
cp -r ~/credential/cloudflare.json ./package
cp -r ../model.onnx ./package
cp -r requirements.txt ./package
cd package && zip -r alibaba_inference.zip  . && cd ..
mv package/alibaba_inference.zip ./
rm -rf package