# Analysis

## Performance Analysis

For performance analysis, we currently support the billing duration and two types of latency: response time and end-to-end delay.

We need to use the transformed logs saved in [/dataset]("https://github.com/hd-zhao/serverless_multicloud/tree/main/dataset"), processed by [/logging_query]("https://github.com/hd-zhao/serverless_multicloud/tree/main/logging_query").

Pinrt CDF figure of billing duration

```bash
python analysis.py -f cdf_bd -a thumbnail-512
```

Pinrt CDF figure of latency

```bash
python analysis.py -f cdf_latency -a thumbnail-512 -l e2e_delay
```


## Cost Analysis

show each part of cost in text:

```bash
python analysis.py -f cost -a thumbnail-512 -d 0.000482 -n 1000000
```

show each part of cost in figure:

```bash
python analysis.py -f cost_detail_figure -a thumbnail-512 -d 0.000482 -n 1000000
```

## Performance and Cost co-analysis

```bash
python analysis.py -f performance_cost -a thumbnail -m 512 -m 1024 -m 2048 -d 0.000482 -n 1000000
```