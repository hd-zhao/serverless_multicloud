

## query the aws lambda logging in CloudWatch dashboard
In lambda function, we add [object, timestamp] as message, e.g., Benchmark object:cat.png timestamp:1657115411273
```
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

