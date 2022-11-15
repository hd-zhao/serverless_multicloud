
cp -r /credential/cloudflare.json .
cp -r ../model.onnx .
docker build -t inference_aws . 

aws ecr get-login-password --region eu-west-2 | docker login --username AWS --password-stdin {your password}
docker tag  {your registry in Amazon Elastic Container Registry}/inference:latest
docker push {your registry in Amazon Elastic Container Registry}/inference:latest


rm -rf cloudflare.json
rm -rf model.onnx