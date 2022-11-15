import pandas as pd
import argparse
import matplotlib.pyplot as plt
import json
import numpy as np
pd.set_option('display.max_rows', None)

color = {
  "alibaba": '#E2725A',
  "aws": '#FFD55A',
  "google": '#79AEB2'
}

cost_color = {
  "Total cost": '#51acc5',
  "Duration fee": '#58508d',
  "Request fee": '#ff6361',
  "Network traffic fee": '#ffa600'
}

DPI = 1200

def exec_latency(evaluate_provider, application, latency_type, cut_off=None):
  print(latency_type)
  for provider in evaluate_provider:
    data_latency = pd.read_csv("../dataset/"+provider+"-"+application+"-latency.csv")
    stats_df = data_latency.groupby("latency") \
    ["latency"] \
    .agg('count') \
    .pipe(pd.DataFrame) \
    .rename(columns = {"latency": 'frequency'})
    print(stats_df)
    # PDF
    stats_df['pdf'] = stats_df['frequency'] / sum(stats_df['frequency'])
    # CDF
    stats_df['cdf'] = stats_df['pdf'].cumsum()
    stats_df = stats_df.reset_index()
    plt.plot(stats_df["latency"], stats_df["cdf"], color[provider], label=provider, linewidth=1)
    if(cut_off!=None):
      plt.xlim(left=0, right=cut_off)
  plt.ylabel('CDF')
  if(latency_type=="e2e_delay"):
    plt.xlabel('End-to-end delay (ms)')
  elif(latency_type=="response_time"):
    plt.xlabel('Response time (ms)')
  plt.legend()
  plt.savefig("figure/"+application+"-latency.pdf", format='pdf', dpi=DPI, bbox_inches='tight')
    




#calculate the billing duration cdf
def exec_billing_duration(evaluate_provider, application, cut_off=None):
  print("Billing-duration")
  for provider in evaluate_provider:
    data = pd.read_csv("../dataset/"+provider+"-"+application+"-bill.csv")
    column1 = provider+"-"+application+"-billingduration"

    stats_df = data.groupby(column1) \
    [column1] \
    .agg('count') \
    .pipe(pd.DataFrame) \
    .rename(columns = {column1: 'frequency'})
    # PDF
    stats_df['pdf'] = stats_df['frequency'] / sum(stats_df['frequency'])
    # CDF
    stats_df['cdf'] = stats_df['pdf'].cumsum()
    stats_df = stats_df.reset_index()
    print(stats_df)
    plt.plot(stats_df[column1], stats_df["cdf"], color[provider], label=provider, linewidth=1)
    if(cut_off!=None):
      plt.xlim(left=0, right=cut_off)

  plt.ylabel('CDF')
  plt.xlabel('Billing Duration (ms)')
  plt.legend()
  plt.savefig("figure/"+application+"-billingduration.pdf", format='pdf', dpi=DPI, bbox_inches='tight')


def cost_analysis(provider, application, request_num, data_size):
  #load FaaS cost model
  pricing_file = json.load(open("../cost_model/faas.json"))
  #loading billing data
  data_memory = pd.read_csv("../dataset/"+provider+"-"+application+"-bill.csv")

  #duration fee
  free_gbs = pricing_file[provider]["free-gbs"]
  gbs_price = pricing_file[provider]["gbs"]
  #request fee
  free_request = pricing_file[provider]["free-request"]
  request_price = pricing_file[provider]["request"]
  #network traffic fee
  network_traffic_price = pricing_file[provider]["network"]
  free_network = pricing_file[provider]["free-network"]
  #CPU fee
  if provider == "google":
    free_ghz = pricing_file[provider]["free-ghz"]
    ghz_price = pricing_file[provider]["ghz"]
  
  #average billing duration
  avg_gbs = round(data_memory[provider+"-"+application+"-GBS"].mean(),2)
  avg_bd = round(data_memory[provider+"-"+application+"-billingduration"].mean(),2)
  if provider == 'google':
        avg_ghz = round(data_memory[provider+"-"+application+"-GHZS"].mean(),2)

  #without free-tier
  request_fee = round(request_price*request_num,2)
  network_fee = round(request_num*network_traffic_price*data_size,2)
  duration_fee = round(gbs_price*request_num*avg_gbs,2)

  if provider == "google":
    ghz_fee = round(avg_ghz*request_num*ghz_price,2)
    duration_fee += ghz_fee
  total_fee = round(request_fee + network_fee + duration_fee,2)

  #with free-tier
  if(request_num<=free_request):
    free_request_fee = 0
  else:
    free_request_fee = round(request_price*(request_num-free_request),2)
  
  if(avg_gbs*request_num<=free_gbs):
    free_duration_fee = 0
  else:
    free_duration_fee = round(gbs_price*(avg_gbs*request_num-free_gbs),2)
  
  if(request_num*data_size<=free_network):
    free_network_fee = 0
  else:
    free_network_fee = round((request_num*data_size-free_network)*network_traffic_price,2)
  
  if(provider == "google"):
    if(avg_ghz*request_num<=free_ghz):
      free_ghz_fee = 0
    else:
      free_ghz_fee = round((avg_ghz*request_num-free_ghz)*ghz_price,2)
    free_duration_fee += free_ghz_fee
  free_total_fee = round(free_request_fee+ free_duration_fee+ free_network_fee,2)

  print(provider)
  print(f"total fee: {total_fee}, duration fee: {duration_fee}, network fee: {network_fee}, request fee: {request_fee}")
  print(f"with free tier, total fee: {free_total_fee}, duration fee: {free_duration_fee}, network fee: {free_network_fee}, request fee: {free_request_fee}")
  print(f"avg billing duration: {avg_bd}")
  print()
  return total_fee, duration_fee, network_fee, request_fee, free_total_fee, free_duration_fee, free_network_fee, free_request_fee, avg_bd

def cost_detail_figure(evaluate_provider, application, request_num, data_size):
  labels = ["Total cost","Duration fee","Request fee", "Network traffic fee"]
  width = 0.2
  position = []
  for x in range(0,4):
    position.append(round(-(width+width/2)+width*x,1))
  provider_len = len(evaluate_provider)

  X_axis = np.arange(len(evaluate_provider))
  value_total_cost = []
  value_duration_fee = []
  value_network_fee = []
  value_request_fee = []

  for provider in evaluate_provider:
    total_fee, duration_fee, network_fee, request_fee, free_total_fee, free_duration_fee, free_network_fee, free_request_fee, avg_bd \
    = cost_analysis(provider, application, request_num, data_size)
    value_total_cost.append(total_fee)
    value_duration_fee.append(duration_fee)
    value_network_fee.append(network_fee)
    value_request_fee.append(request_fee)


  plt.bar(X_axis+position[0], value_total_cost, width, color = cost_color["Total cost"], label="Total cost")
  plt.bar(X_axis+position[1], value_duration_fee, width, color = cost_color["Duration fee"], label="Duration fee")
  plt.bar(X_axis+position[2], value_network_fee, width, color = cost_color["Network traffic fee"], label="Network traffic fee")
  plt.bar(X_axis+position[3], value_request_fee, width, color = cost_color["Request fee"],label="Request fee")
  plt.xticks(X_axis,evaluate_provider)
  plt.xlabel("Provider")
  plt.ylabel('1M requests cost ($)')
  plt.legend()
  plt.savefig("figure/"+application+"-cost_detail.pdf", format='pdf', dpi=DPI, bbox_inches='tight')
    
def performance_cost(evaluate_provider, application, memory_array, request_num, data_size):

  value_bd = {}
  value_cost = {}
  for provider in evaluate_provider:
    value_bd[provider] = []
    value_cost[provider] = []
  for memory in memory_array:
    for provider in evaluate_provider:
      dataset_name = application + "-" + memory
      total_fee, duration_fee, network_fee, request_fee, free_total_fee, free_duration_fee, free_network_fee, free_request_fee, avg_bd \
      = cost_analysis(provider, dataset_name, request_num, data_size)
      value_bd[provider].append(avg_bd)
      value_cost[provider].append(total_fee)
  
  X_axis = np.arange(len(memory_array))
  width = 0.2
  position = [-width, 0, width]
  
  fig, ax = plt.subplots()
  ax2 = ax.twinx()
  for i in range(0,len(evaluate_provider)):
    ax.bar(X_axis+position[i], value_bd[evaluate_provider[i]], width, color = color[evaluate_provider[i]], label=evaluate_provider[i])

  for i in range(0,len(evaluate_provider)):
    ax2.plot(X_axis, value_cost[evaluate_provider[i]], color = color[evaluate_provider[i]], label=evaluate_provider[i], linewidth=1)
  ax.set_ylim(top=1200)
  ax2.set_ylim(bottom=0, top=16)
  plt.xticks(X_axis, memory_array)
  ax.set_xlabel("Memory size (MB)")
  plt.ylabel('Avg. billing duration (ms)')
  ax.set_ylabel('Avg. billing duration (ms)')
  ax2.set_ylabel('1M requests total cost ($)')
  plt.legend(loc='upper center', ncol=len(evaluate_provider))
  plt.savefig("figure/"+application+"-cost_performance_co_analysis.pdf", format='pdf', dpi=DPI, bbox_inches='tight')

  
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--provider", action="append", dest="provider", default=[], 
                        help="analysis provider")

    parser.add_argument("-a", "--application", dest="application", default="thumbnail",
                        help="analysis application")

    parser.add_argument("-f", "--figure_type", dest="figure_type", default=None,
                        help="cdf_bd, cdf_latency, cost, cost_detail_figure, performance_cost")
    
    parser.add_argument("-l", "--latency", dest="latency", default="e2e_delay",
                        help="latency class")
    
    parser.add_argument("-d", "--data_size", dest="data_size", type=float, default=0,
                        help="egress data size")
    
    parser.add_argument("-n", "--request_num", dest="request_num", type=int, default=1000000,
                        help="request_num")
    

    parser.add_argument("-m", "--memory", action="append", dest="memory", default=[],
                        help="memory selection for plot")

    parser.add_argument("-cut_off", "--cut_off", dest="cut_off", default=None,
                        help="cut off value of billing duration")


    args = parser.parse_args()

    if len(args.provider) == 0:
        args.provider = ["aws","google","alibaba"]

    if(args.figure_type == "cdf_bd"):
      exec_billing_duration(args.provider, args.application, args.cut_off)
    elif(args.figure_type == "cdf_latency"):
      exec_latency(args.provider,args.application, args.latency, args.cut_off)
    elif(args.figure_type == "cost"):
      for evaluate_provider in args.provider:
        cost_analysis(evaluate_provider, args.application, args.request_num, args.data_size)
    elif(args.figure_type == "cost_detail_figure"):
      cost_detail_figure(args.provider, args.application, args.request_num, args.data_size)
    elif(args.figure_type == "performance_cost"):
      performance_cost(args.provider, args.application, args.memory, args.request_num, args.data_size)

      
      
    

    