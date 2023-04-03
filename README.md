# Code
**Supporting Multi-Cloud in Serverless Computing**

**[[Paper](https://ieeexplore.ieee.org/document/10061782)]**
**[[Arxiv](https://arxiv.org/abs/2209.09367)]**
**[[HAL-Inria](https://hal.inria.fr/hal-03945892/file/arxiv.pdf)]**

**Abstract:**
Serverless computing is a widely adopted cloud execution model composed of Function-as-a-Service (FaaS) and Backend-as-a-Service (BaaS) offerings. The increased level of abstraction makes vendor lock-in inherent to serverless computing, raising more concerns than previous cloud paradigms. Multi-cloud serverless is a promising emerging approach against vendor lock-in, yet multiple challenges must be overcome to tap its potential. First, we need to be aware of both the performance and cost of each FaaS provider. Second, a multi-cloud architecture must be proposed before deploying a multi-cloud workflow. Domain-specific serverless offerings must then be integrated into the multi-cloud architecture to improve performance or save costs. Moreover, dealing with serverless offerings from multiple providers is challenging. Finally, we require workload portability support for serverless multi-cloud.
In this paper, we present a multi-cloud library for cross-serverless offerings. We develop the End Analysis System (EAS) to support comparison among public FaaS providers in terms of performance and cost. Moreover, we design proof-of-concept multi-cloud architectures with domain-specific serverless offerings to alleviate problems such as data gravity. Finally, we deploy workloads on these architectures to evaluate several public FaaS offerings.
