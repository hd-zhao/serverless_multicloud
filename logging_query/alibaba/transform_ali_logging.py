import pandas as pd
import argparse


def roundup(x):
    if(x%100 == 0):
        return int(x)
    else:
        return int(x + 100 - x % 100)

def excute_mem(gbs_data, dataset_name,memory_usage=None):
    save_data = pd.DataFrame([])
    dataset= gbs_data
    data = pd.read_csv(dataset+"-mem.csv")
    data['timestamp'] = data.invocationStartTimestamp.astype(int)
    thumbnail_data = pd.DataFrame([])
    data['time_usage'] = data['durationMs'].apply(lambda x: roundup(x))
    print(data)


    thumbnail_data["alibaba-"+dataset_name+"-timestamp"] = data['timestamp']
    thumbnail_data["alibaba-"+dataset_name+"-GBS"] = round(data['time_usage']/1000*memory_usage/1024,2)
    thumbnail_data["alibaba-"+dataset_name+"-billingduration"] = data['time_usage'].astype(int)
    intermediate_name = "alibaba-"+dataset_name+"-timestamp"
    thumbnail_data = thumbnail_data.sort_values(by=intermediate_name,ascending=True)
    save_data = pd.concat([save_data, thumbnail_data],axis=1)
    
    path = "../../dataset/"+"alibaba-"+dataset_name+"-bill.csv"
    save_data.to_csv(path,index=False)


def excute_latency(latency_data,dataset_name):
    save_data = pd.DataFrame([])
    
    data1 = pd.read_csv(latency_data+"-latency.csv")
    data_logging = pd.read_csv("logging-ali-"+latency_data+".csv")
    data = pd.DataFrame([])
    column1 = "alibaba-"+dataset_name+"-object"
    column2 = "alibaba-"+dataset_name+"-timestamp"
    data["object"] = data1['message'].str.split().str[2]
    data["alibaba-"+dataset_name+"-timestamp"] = data1['message'].str.split().str[4]

    
    right_join_df = pd.merge(data_logging, data, on='object', how='right')
    right_join_df[column2] = right_join_df[column2].astype(int)
    right_join_df["timestamp"] = right_join_df["timestamp"].astype(int)
    #print(right_join_df[column2]-right_join_df["timestamp"])
    save_data["latency"] = right_join_df[column2]-right_join_df["timestamp"]
    save_data["object"] = right_join_df['object']
    print(save_data.sort_values(by=['latency']))

    path = "../../dataset/"+"alibaba-"+dataset_name+"-latency.csv"
    save_data.to_csv(path,index=False)
    
        


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-m", "--configure_memory", dest="mem", type=int, default=1024,
                        help="serverless function memory allocate")
    parser.add_argument("-g", "--general", dest="general_gbs", default=None,
                        help="transform general task memory log")
    parser.add_argument("-gl", "--general_latency", dest="general_latency", default=None,
                        help="transform general task latency log")

    args = parser.parse_args()



    if args.general_latency != None:
        excute_latency(args.general_latency,args.general_latency)
    if args.general_gbs != None:
        excute_mem(args.general_gbs,args.general_gbs,args.mem)

