import argparse,json
from object_storage_trigger import update_operation

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--provider", dest="provider", default= None,
                        help="benchmark provider")
    
    parser.add_argument("-tn", dest="thumbnail", default="5mb",
                        help="image resize application")
    
    parser.add_argument("-n", "--normalization_invoke", dest="nor", default=None,
                        help="normalization, please direct input the invoke number, configured in json file")
    parser.add_argument("-t", "--ml_training_invoke", dest="mlt", default=None,
                        help="ml training, please direct input the invoke number, configured in json file")
    args = parser.parse_args()

    if args.provider == None:
        print("please input the provider")
        exit()
    
    if args.nor != None:
        print("normalization benchmarking!")
        if args.provider == "multicloud":
            print("hello")
        else:
            http_exec(args.provider,args.nor,"normalization")

    if args.mlt != None:
        print("ml training benchmarking!")
        if args.provider == "multicloud":
            print("hello")
        else:
            http_exec(args.provider,args.mlt,"mltraining")
    


    if args.thumbnail != None:
        print(f"Provider:{args.provider} image resize application!")
        config = json.load(open("./benchmark_configuration/thumbnail.json"))
        update_operation(args.provider, \
                        config[args.provider]["credential"],    \
                        config[args.provider][args.thumbnail]['bucket'],  \
                        config[args.provider][args.thumbnail]['picture'],   \
                        "thumbnail")
        