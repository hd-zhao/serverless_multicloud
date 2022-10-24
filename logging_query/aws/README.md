
# Cloud logs Query: AWS Lambda

## Login to the CloudWatch

<img
  src="https://github.com/hd-zhao/serverless_multicloud/blob/main/asset/aws1.png"
  alt="Alt text"
  title="Enter into CloudWatch"
  style="display: inline-block; margin: 0 auto; max-width: 300px">

## query the aws lambda logging in CloudWatch dashboard

In lambda function, we add [object, timestamp] as message, e.g., Benchmark object:cat.png timestamp:1657115411273
```bash
        #query logging:billing cost, etc.
        filter @type = "REPORT"
        | fields @timestamp as Timestamp, @requestId as RequestID, @billedDuration as BilledDurationInMS, @memorySize/1000000 as MemorySetInMB, @billedDuration/1000*MemorySetInMB/1024 as BilledDurationInGBSeconds
        | sort Timestamp asc
        | limit 2000

        #query logging:timestamp
        filter @message like /Benchmark/
        | parse '* *:* *:*' as benchmark, object_symbol, object, timestamp_symbol,timestamp
        | limit 2000
```

