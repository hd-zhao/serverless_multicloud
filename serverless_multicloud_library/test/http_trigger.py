import sys 
import os
import json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

#from src.trigger import alibaba_trigger
from src.trigger import aws_trigger
from src.trigger import google_trigger
from src.trigger import alibaba_trigger

#aws http trigger

#return_msg = aws_trigger.invoke("../../credential/aws.json",'function1',"sync",json.dumps("asd"))
#my_json = return_msg['Payload'].read().decode('utf8')
#data = json.loads(my_json)
#print(int(data['timestamp']))
#google_end_point = "https://europe-west2-amiable-bridge-342803.cloudfunctions.net/function-1c"
#return_msg = google_trigger.invoke("../../credential/google_cloud.json",'function-1c',"sync",json.dumps("asd"),google_end_point)
#data = json.loads(return_msg.text)
#print(data['object'])
#alibaba_end_point = 'https://funca-service-bazchomcjg.eu-west-1.fcapp.run'
alibaba_trigger.invoke("../../credential/alibaba.json",'func1a',"sync",json.dumps("asd"),alibaba_end_point)