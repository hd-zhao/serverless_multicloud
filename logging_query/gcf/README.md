# Cloud logs Query: Google Cloud Function

## query the google cloud function logging in dashboard

```bash
#query the exection time for 1st generation FaaS
<default query here>
"Function"
"execution"
"took"

#query the function logging

In google cloud function, add [object, timestamp] for logging to measure the latency, e.g., Benchmark object:cat.png timestamp:1657115411273

<default query here>
"Benchmark"
```

<img
  src="https://github.com/hd-zhao/serverless_multicloud/blob/main/asset/gcf1.png"
  alt="Alt text"
  title="Enter into CloudWatch"
  style="display: inline-block; margin: 0 auto; max-width: 200px">



## transform Google logs

Save cloud logs and local logs in [/log](https://github.com/hd-zhao/serverless_multicloud/tree/main/logging_query/log)

For end-to-end delay, take thumbnail as an example:

```bash
bash output.sh thumbnail-512 e2e_delay 512
```

For resonse time, take thumbnail as an example:

```bash
bash output.sh thumbnail-512 response_time 512
```