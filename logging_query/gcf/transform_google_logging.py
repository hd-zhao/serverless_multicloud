import pandas as pd
import argparse


def roundup(x):
    return x if x % 100 == 0 else x + 100 - x % 100

def srt_split(x):
    return float(str(x[:-1]))*1000

def excute_mem(gbs_data, dataset_name,memory_usage=None):
    save_data = pd.DataFrame([])
    dataset = gbs_data
    data = pd.read_csv(dataset+"-mem.csv")
    data.timestamp = pd.to_datetime(data.timestamp).astype(int)/10**9
    data.timestamp = data.timestamp.astype('int')
    thumbnail_data = pd.DataFrame([])
    data['time_usage'] = data['textPayload'].str.extract('(\d+)').astype('int')
    data['time_usage'] = data['time_usage'].apply(lambda x: roundup(x))
    thumbnail_data["google-"+dataset_name+"-timestamp"] = data['timestamp']
    thumbnail_data["google-"+dataset_name+"-GBS"] = data['time_usage']/1000*memory_usage/1024
    if memory_usage == 1024:
        ghzs_value = 1.4
    elif memory_usage == 128:
        ghzs_value = 0.1992
    elif memory_usage == 256:
        ghzs_value = 0.4008
    elif memory_usage == 512:
        ghzs_value = 0.7992
    elif memory_usage == 2048:
        ghzs_value = 2.4
    elif memory_usage == 4096 or memory_usage == 8192:
        ghzs_value =2.4
    thumbnail_data["google-"+dataset_name+"-GHZS"] = round(data['time_usage']/1000*ghzs_value,2)
    thumbnail_data["google-"+dataset_name+"-billingduration"] = data['time_usage']
    intermediate_name = "google-"+dataset_name+"-timestamp"
    thumbnail_data = thumbnail_data.sort_values(by=intermediate_name,ascending=True)
    save_data = pd.concat([save_data, thumbnail_data],axis=1)
    
    path = "../../dataset/"+"google-"+dataset_name+"-bill.csv"
    save_data.to_csv(path,index=False)

def excute_mem_2(gbs_data, dataset_name,memory_usage=None):
    save_data = pd.DataFrame([])
    dataset = gbs_data
    data = pd.read_csv(dataset+"-mem.csv")
    #data.timestamp = pd.to_datetime(data.protoPayload.response.metadata.creationTimestam).astype(int)/10**9
    #data.timestamp = data.timestamp.astype('int')
    thumbnail_data = pd.DataFrame([])
    data['time_usage'] = data['httpRequest.latency']
    data['time_usage'] = data['time_usage'].apply(lambda x:srt_split(x)).astype('int')

    print(data['time_usage']) 

    #.astype('int')
    data['time_usage'] = data['time_usage'].apply(lambda x: roundup(x))
    thumbnail_data["google-"+dataset_name+"-timestamp"] = data['timestamp']
    thumbnail_data["google-"+dataset_name+"-GBS"] = data['time_usage']/1000*memory_usage/1024
    thumbnail_data["google-"+dataset_name+"-GHZS"] = round(data['time_usage']/1000*200*(memory_usage/128)/1000,2)
    thumbnail_data["google-"+dataset_name+"-billingduration"] = data['time_usage']
    intermediate_name = "google-"+dataset_name+"-timestamp"
    thumbnail_data = thumbnail_data.sort_values(by=intermediate_name,ascending=True)
    save_data = pd.concat([save_data, thumbnail_data],axis=1)
    
    path = "../../dataset/"+"google-"+dataset_name+"-bill.csv"
    save_data.to_csv(path,index=False)

def excute_latency(latency_data,dataset_name):
    save_data = pd.DataFrame([])
    
    data1 = pd.read_csv(latency_data+"-latency.csv")
    #print(data1['textPayload'])
    data_logging = pd.read_csv("logging-google-"+latency_data+".csv")
    data = pd.DataFrame([])
    column1 = "google-"+dataset_name+"-object"
    column2 = "google-"+dataset_name+"-timestamp"
    data["object"] = data1['textPayload'].str.split().str[2]
    data["google-"+dataset_name+"-timestamp"] = data1['textPayload'].str.split().str[4]
    print(data)
    right_join_df = pd.merge(data_logging, data, on='object', how='right')
    right_join_df[column2] = right_join_df[column2].astype(int)
    right_join_df = right_join_df.fillna(0)
    right_join_df["timestamp"] = right_join_df["timestamp"].astype(int)
    #print(right_join_df[column2]-right_join_df["timestamp"])
    save_data["latency"] = right_join_df[column2]-right_join_df["timestamp"]
    save_data["object"] = right_join_df['object']
    print(save_data)

    path = "../../dataset/"+"google-"+dataset_name+"-latency.csv"
    save_data.to_csv(path,index=False)
        


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    
    parser.add_argument("-m", "--configure_memory", dest="mem", type=int, default=1024,
                        help="serverless function memory allocate")
                        
    parser.add_argument("-g", "--general", dest="general_gbs", default=None,
                        help="transform general task memory log")
    
    parser.add_argument("-n", "--general_2", dest="general_gbs2", default=None,
                        help="transform general task memory log2")

    parser.add_argument("-gl", "--general_latency", dest="general_latency", default=None,
                        help="transform general task latency log")




    args = parser.parse_args()

    if args.general_gbs != None:
        excute_mem(args.general_gbs,args.general_gbs,args.mem)

    if args.general_gbs2 != None:
        excute_mem_2(args.general_gbs2,args.general_gbs2,args.mem)

    if args.general_latency != None:
        excute_latency(args.general_latency,args.general_latency)


