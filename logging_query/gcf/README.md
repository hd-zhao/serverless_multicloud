## query the google cloud function logging in dashboard

```
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
move the local logging of google cloud function from parent directory to the current directory

transform the dataset of logging.
```

```


    