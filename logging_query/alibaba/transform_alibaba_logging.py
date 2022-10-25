import pandas as pd
import argparse


def roundup(x):
    if(x%100 == 0):
        return int(x)
    else:
        return int(x + 100 - x % 100)

def excute_mem(dataset_name):
    save_data = pd.DataFrame([])
    transform_data = pd.DataFrame([])

    data = pd.read_csv("../log/alibaba-"+dataset_name+"-mem.csv")
    data['timestamp'] = data.invocationStartTimestamp.astype(int)
    data['time_usage'] = data['durationMs'].apply(lambda x: roundup(x))
    memory_usuage = data.iloc[0].memoryMB

    transform_data["alibaba-"+dataset_name+"-timestamp"] = data['timestamp']
    transform_data["alibaba-"+dataset_name+"-GBS"] = round(data['time_usage']/1000*memory_usuage/1024,2)
    transform_data["alibaba-"+dataset_name+"-billingduration"] = data['time_usage'].astype(int)

    intermediate_name = "alibaba-"+dataset_name+"-timestamp"
    transform_data = transform_data.sort_values(by=intermediate_name,ascending=True)
    save_data = pd.concat([save_data, transform_data],axis=1)
    
    path = "../../dataset/"+"alibaba-"+dataset_name+"-bill.csv"
    save_data.to_csv(path,index=False)


def e2e_latency(dataset_name):
    save_data = pd.DataFrame([])
    data = pd.DataFrame([])

    data1 = pd.read_csv("../log/alibaba-"+dataset_name+"-latency.csv")
    data_logging = pd.read_csv("../log/alibaba-"+dataset_name+".csv")
    
    column1 = "alibaba-"+dataset_name+"-object"
    column2 = "alibaba-"+dataset_name+"-timestamp"
    data["object"] = data1['message'].str.split().str[1].str.split(':').str[1]
    data["alibaba-"+dataset_name+"-timestamp"] = data1['message'].str.split().str[2].str.split(':').str[1]

    right_join_df = pd.merge(data_logging, data, on='object', how='right')
    right_join_df[column2] = right_join_df[column2].astype(int)
    right_join_df["timestamp"] = right_join_df["timestamp"].astype(int)
    #print(right_join_df[column2]-right_join_df["timestamp"])
    save_data["latency"] = right_join_df[column2]-right_join_df["timestamp"]
    save_data["object"] = right_join_df['object']

    path = "../../dataset/"+"alibaba-"+dataset_name+"-latency.csv"
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