# Workload Adapter & Local Logging

## Workload

We assume that the invocation is complied with poisson arrival instead of burst workloads. Besides, as the released [Azure Functions Trace](https://github.com/Azure/AzurePublicDataset/blob/master/AzureFunctionsDataset2019.md) reveals, most serverless applications are invoked infrequently, e.g., 81% of the applications are invoked less than once per minute on average. With a default concurrency limit (e.g., AWS Lambda supports 1000 concurrent requests), public FaaS providers should be able to handle the majority of workloads with ease.

## Local logging

We support two latency classes: end-to-end delay and response time, you can opt for one in command line by `-l e2e_delay` and `response_time`, respectively.

## HTTP trigger

To invoke Google Cloud Functions, it needs an endpoint that is configured in the `~/credential/google_cloud.json` file. We use the unauthorized type of function.

## Application Benchmarks 

### Image Resize: thumbnail

The invocation frist upload an object to object storage. This operation then trigger a function instance to retrieve from the object storage service and process it.

AWS Lambda: 

```bash
python adapter.py -p aws -s object_storage -a thumbnail -mu 0.1  -t 20 -m 1024 -o upload -l e2e_delay
```

Google Cloud Function: 

```bash
python adapter.py -p google -s object_storage -a thumbnail -mu 0.1  -t 20 -m 1024 -o upload -l e2e_delay
```

Alibaba Function Compute:

```bash
python adapter.py -p alibaba -s object_storage -a thumbnail -mu 0.1  -t 20 -m 1024 -o upload -l e2e_delay
```
### Image Resize: thumbnail (HTTP trigger) for comparison

AWS Lambda: 

```bash
python adapter.py -p aws -s http -a thumbnail-http -mu 0.1  -t 20 -m 1024 -l e2e_delay
```

Google Cloud Function: 

```bash
python adapter.py -p google -s http -a thumbnail-http -mu 0.1  -t 20 -m 1024 -l e2e_delay
```

Alibaba Function Compute:

```bash
python adapter.py -p alibaba -s http -a thumbnail-http -mu 0.1  -t 20 -m 1024 -l e2e_delay
```
