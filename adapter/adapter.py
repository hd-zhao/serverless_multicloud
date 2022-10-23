import argparse,json
import object_storage
import cloud_function
import sys

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--provider", dest = "provider", default= None,
                        help = "benchmark provider")

    parser.add_argument("-s","--serverless_offering",dest = "so", default = None, 
                        help = "Serverless Offerings: FaaS and BaaS")

    parser.add_argument("-a","--benchmarked_applications",dest = "application", default = None, 
                        help = "Application-oriented benchmark")
    
    parser.add_argument("-mu", "--mu", dest = "mu", default = None, type=float,
                        help = "poisson rate")

    parser.add_argument("-t","--minute",dest = "minute", default = None, type=int,
                        help = "Benchmark duration")

    parser.add_argument("-m","--memory",dest = "memory", default = None, 
                        help = "Memory allocation")
    
    parser.add_argument("-l","--latency",dest = "latency_category", default = None, 
                        help = "Latency Category")
    
    parser.add_argument("-o","--operation",dest = "operation", default = None, 
                        help = "Opertions in BaaS offerings")

    args = parser.parse_args()

    try:
        config = json.load(open("./benchmark_configuration/" + args.application + ".json"))
        print(f"Application:{args.application}")
    except Exception as e:
        print("Please configure the application in the ./benchmark_configuration first")
        exit()
    

    if args.so == "object_storage":
        object_storage.operation(args.provider, 
                                config[args.provider]["credential"],    
                                config[args.provider]['bucket'],  
                                config[args.provider]['object'],   
                                args.application,
                                args.mu,
                                args.memory,
                                args.latency_category,
                                args.operation,
                                args.minute)

    else:
        print("Please input correct serverless offerings.")
        exit()

