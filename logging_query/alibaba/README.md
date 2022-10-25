# Cloud logs Query: Alibaba Function Compute

## query the logs in the dashboard

```bash
serviceName:service1 AND functionName:function9 AND durationMs NOT FunctionUnhandledError
serviceName:service1 AND functionName:function9 AND "Benchmark"
```

<img
  src="https://github.com/hd-zhao/serverless_multicloud/blob/main/asset/afc1.png"
  alt="Alt text"
  title="Enter into CloudWatch"
  style="display: inline-block; margin: 0 auto; max-width: 200px">

## transform Alibaba Function Compute logs

Save cloud logs and local logs in [/log](https://github.com/hd-zhao/serverless_multicloud/tree/main/logging_query/log)

For end-to-end delay, take thumbnail as an example:

```bash
bash output.sh thumbnail-1024 e2e_delay
```

For response time, take thumbnail as an example:

```bash
bash output.sh thumbnail-1024 response_time
```