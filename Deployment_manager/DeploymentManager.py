from time import sleep
from json import dumps
import json
import threading

import sys
sys.path.insert(0, "../communication_module")

import communication_module as cm


sensor_id_returned={	1:{"topic":"Temperatue",
						"id":"s104"},

						2:{"topic":"Humidity",
						"id":"t808"},
					}



def handle_servicelc_msg(msg):

	print("Service Recieved to deploy:-\n",msg)

	request_sensor(msg)

	# sensors=msg_recieved_sensor_mgr()

	# msg['algoid']['sensor']=sensors

	# generate_dockerfile(msg)

		


def generate_dockerfile(msg):
	f=open('Services/'+str(msg['reqid'])+'.dockerfile',"w")
	f.write("FROM python:3.7-alpine\n")
	f.write("COPY . /src\n")
	f.write("WORKDIR /src/\n")
	f.write(" CMD ['"' pyhton3 '"'," +'"'+  msg["algoid"]["path"]  +'"'+","+'"'+msg["algoid"]["sensor"][1]["topic"] +'"'+"]")

def send_to_server(data):
	cmd=""
	cmd=cmd+"../"+str(data['algoid']['path'])+" "
	cmd=cmd+" "+str(data['UserID'])+" "+str(data['AppName'])+" "+str(data['Action_type'])+" "
	cmd=cmd+str(data['topics'][0])+" "+str(data['ids'][0])+" "
	cmd=cmd+str(data['location'])
	cmd
	mess={}
	mess['service_id']=str(data['server_id'])
	mess['code']=str(cmd)
	cm.DeployManager_to_RuntimeServer_Producer_interface(mess)
	print("\nSending to Run Time server :-\n",cmd)


def request_sensor(data):

	print("\nSending to Sensor mgr :-\n")
	cm.DeployManager_to_SensorManager_Producer_interface(data)
		


def handle_sensor_mgr_msg(msg):
	print("Recived Sensor details")
	# generate_dockerfile(msg)
	send_to_server(msg)

def msg_recieved_sensor_mgr():
	return sensor_id_returned



th=threading.Thread(target=cm.ServiceLifeCycle_to_DeployManager_interface,kwargs={'func_name':handle_servicelc_msg})
th.start()


th=threading.Thread(target=cm.SensorManager_to_DeployManager_interface,kwargs={'func_name':handle_sensor_mgr_msg})
th.start()
# cm.ServiceLifeCycle_to_DeployManager_interface(handle_servicelc_msg)
