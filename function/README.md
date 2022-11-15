# Deployment guide

We need to import libary into the function instance.

AWS: manually download then add it into the .zip file for small size packages. For big size library, it need to use docker to register.

Google: It can directly add the required library into the requirements.txt

Alibaba: We recommend to use layer to configure the library. It is convinient.