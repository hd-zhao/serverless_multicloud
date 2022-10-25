import pandas as pd
import argparse


def excute_mem(dataset_name):
    save_data = pd.DataFrame([])
    data=pd.read_csv("../log/"+dataset_name+"-mem.csv")
    data.Timestamp = pd.to_datetime(data.Timestamp).astype(int)/10**6
    data.Timestamp = data.Timestamp.astype('int')
    transform_data = pd.DataFrame([])
    transform_data["aws-"+dataset_name+"-timestamp"] = data.Timestamp 
    transform_data["aws-"+dataset_name+"-GBS"] = data.BilledDurationInGBSeconds
    transform_data["aws-"+dataset_name+"-billingduration"] = data.BilledDurationInMS
    save_data = pd.concat([save_data, transform_data],axis=1)
    path = "../../dataset/"+"aws-"+dataset_name+"-bill.csv"
    save_data.to_csv(path,index=False)

def e2e_latency(dataset_name):

    save_data = pd.DataFrame([])
    data = pd.read_csv("../log/"+dataset_name+"-latency.csv")
    data_logging = pd.read_csv("../log/aws-"+dataset_name+".csv")
    
    column1 = "aws-"+dataset_name+"-object"
    column2 = "aws-"+dataset_name+"-timestamp"
    transform_data = pd.DataFrame([])
    transform_data["object"] = data.object
    transform_data["aws-"+dataset_name+"-timestamp"] = data.timestamp.astype(int)
    data_logging.timestamp = data_logging.timestamp.astype(int)
    right_join_df = pd.merge(data_logging, transform_data, on='object', how='right')
    save_data["latency"] = right_join_df[column2]-right_join_df["timestamp"]
    save_data["object"] = right_join_df['object']
    path = "../../dataset/"+"aws-"+dataset_name+"-latency.csv"
    save_data.to_csv(path,index=False)



if __name__ == "__main__":
    parser = argparse.ArgumentParser()


    parser.add_argument("-g", "--general", dest="general_gbs", default=None,
                        help="transform general task memory log")

    parser.add_argument("-l", "--latency_class", dest="latency", default=None,
                        help="transform latency log")

    parser.add_argument("-d", "--dataset", dest="dataset", default=None,
                        help="input dataset")
    args = parser.parse_args()


    if args.general_gbs != None:
        excute_mem(args.general_gbs)
    
    if args.latency == "e2e_delay":
        e2e_latency(args.dataset)
