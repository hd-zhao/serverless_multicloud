FROM public.ecr.aws/lambda/python:3.9


# Copy function code
COPY index.py ${LAMBDA_TASK_ROOT}

# Install the function's dependencies using file requirements.txt
# from your project folder.

COPY model.onnx ${LAMBDA_TASK_ROOT}
COPY cloudflare.json ${LAMBDA_TASK_ROOT}
COPY requirements.txt  .
RUN  pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "index.handler" ]