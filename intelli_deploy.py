import sys
import os
from os import path
import shutil
import zipfile as zp
import re
import pyutil
import json
import requests
import upload_n_deploy
import zip_n_unzip
import creating_kvm
from create_data_collector import Dc_store
from handling_target_servers import Handling_Target_Servers
from edit_shared_flow import Edit_Shared_Flow
from edit_statistic_collector import Edit_Statistic_Collector
from edit_spike_arrest import Edit_Spike_Arrest
from edit_message_logging import Edit_Message_Logging

filename=""
current_path = ""
bearer_token =""

with open("config.json") as json_data_file:
    data = json.load(json_data_file)
current_path= data['path']
bearer_token =data['token']
org=data['org_name']
environment=data['environment']
host=data['host']
port=data['port']
message_log=data['log_message']
no_of_mp=data['message_processor']
src_dc_file=data['source_file_data_capture']

count_of_resources=0
count_of_sf=0
proxies_folder_path=current_path+"\\proxies"

createkvm=creating_kvm
kvm_folder_path="kvm"
createkvm.Createkvm.createkvm(current_path,kvm_folder_path,bearer_token,org)

resource_counter=0
no_shared_flows=0
try:
	os.chdir(proxies_folder_path)
	filenames = os.listdir(proxies_folder_path)
	#print(filenames)
	#filenames=['eighth-demo-sam.zip','statistic_collector_r2.zip','mesage_logging_rec2.zip','TS-namedServer.zip']


	for filename in filenames:
		filename =filename.strip()
		filename =re.search(r'(.*?).zip',filename)
		if filename:
			if resource_counter <=50:
				resource_counter = resource_counter +1
				filename = str(filename.group(1))
				print("--------------------------------------------------------------------------------------------")
				print("|                    PROXY COUNT "+str(resource_counter)+" PROXY NAME "+filename)
				print("--------------------------------------------------------------------------------------------")
				
				zip_n_unzip.Unzip.unzip_file(filename,proxies_folder_path+"\\"+filename)
				policy_folder_exist ="False"
				policy_folder_exist=str(path.exists(current_path+"\\proxies"+"\\"+filename+"\\apiproxy\\policies\\"))
				if 	policy_folder_exist =="True":
					try:
						statistic_collector_switch='false'
						message_logging_switch='false'
						shared_flow_switch='false'
						spike_arrest_switch='false'
						os.chdir(current_path+"\\proxies"+"\\"+filename+"\\apiproxy\\policies\\")
						arr = os.listdir()
						for i in arr:
							file2=open(current_path+"\\proxies"+"\\"+filename+"\\apiproxy\\policies"+"\\"+i, 'r')
							lines=file2.readlines()
							for line in lines:
								result_check_sf = re.search(r'\s*<SharedFlowBundle>(.*?)</SharedFlowBundle>',line)
								if result_check_sf:
									name_sf=result_check_sf.group(1).strip()
									shared_flow_switch='true'


									if shared_flow_switch == "true":
										no_shared_flows = no_shared_flows +1
										resource_counter = resource_counter +1
										print("--------------------------------------------------------------------------------------------")
										print("|   SHARED FLOW NAME : "+name_sf+ " PROXY NAME "+filename )                               
										print("--------------------------------------------------------------------------------------------")

										edit_shared_flow=Edit_Shared_Flow
										edit_shared_flow.edit_shared_flow(environment,current_path,name_sf,bearer_token,org)
										zip_n_unzip.Zip.create_newzip_after_changes(filename,proxies_folder_path)
														
								result_check_sc =re.search(r'<StatisticsCollector.*name="(.*?)"',line)
								if result_check_sc:
									name_sc=result_check_sc.group(1).strip()
									proxy_name_include_sc=filename.strip()
									#print("<================ StatisticsCollector found with Name ===================> " +name_sc)
									statistic_collector_switch="true"	

														
								result_spike = re.match(r'<SpikeArrest.*name="(.*?)">', line)
								if result_spike:
									name_sa=result_spike.group(1).strip()
									proxy_name_include_sa=filename.strip()
									#print("<========================= Spike Arrest policy Found with Name ===================>"+name_sa)
									spike_arrest_switch="true"
									if spike_arrest_switch == "true":
										edit_spike_arrest=Edit_Spike_Arrest
										edit_spike_arrest.edit_spike_arrest(current_path,proxy_name_include_sa,name_sa,bearer_token,no_of_mp)
										zip_n_unzip.Zip.create_newzip_after_changes(filename,proxies_folder_path)
														
								matches_name_ml=re.search(r'<MessageLogging .*name="(.*?)"',line)
								if matches_name_ml:
									name_ml=matches_name_ml.group(1)
									proxy_name_include_ml=filename.strip()
									message_logging_switch='true'
									current_file_ml=i
									#print("<======================= Name of Message Logging Policy ==============>" +name_ml)
									if message_logging_switch == "true":
										edit_message_logging=Edit_Message_Logging
										edit_message_logging.edit_message_logging(current_path,proxy_name_include_ml,name_ml,bearer_token,message_log,host,port)
										zip_n_unzip.Zip.create_newzip_after_changes(filename,proxies_folder_path)		

							file2.close()

					except OSError as e:
						print("<================== Policy Folder does not Exists in this PROXY ===================>")
						print("Failed with:", e.strerror) # look what it says
				if statistic_collector_switch=="true":
					edit_statistic_collector=Edit_Statistic_Collector
					edit_statistic_collector.edit_statistic_collector(current_path,proxy_name_include_sc,name_sc,bearer_token,src_dc_file)
					zip_n_unzip.Zip.create_newzip_after_changes(filename,proxies_folder_path)		
				##########################################  Checking for Target Servers  #######################################
				target_server_exist=str(path.exists(proxies_folder_path+"\\"+filename+"\\apiproxy\\targets\\default.xml"))
				#print("<============================ TARGET SERVERS FOUND =============================>"+target_server_exist)
				if target_server_exist =="True":
					handle_ts=Handling_Target_Servers
					handle_ts.create_target_server(current_path,filename)
					zip_n_unzip.Zip.create_newzip_after_changes(filename,proxies_folder_path)
				
				resource_type="apis"
				resource_id = "apiProxyId"
				upload_zip=upload_n_deploy
				upload_zip.Upload.upload_to_hybrid(proxies_folder_path,filename,bearer_token,org,resource_type,resource_id)
				upload_zip.Deploy.deploy_to_hybrid(environment[0],filename,bearer_token,org,resource_type)
			else:
				print("--------------------------------------------------------------------------------------------")
				print("|         !!!      You have Exhausted the quota please try another environment     !!!     |")
				print("--------------------------------------------------------------------------------------------")
				exit()
			
except OSError as e:
	print("<================== File not found PLEASE CHECK config.json file ===================>")
	print("Failed with:", e.strerror)
	
