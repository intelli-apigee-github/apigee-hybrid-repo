import sys
import os
import shutil
import zipfile as zp
import re
#from pyutil import filereplace
import pyutil
import json
import requests
import upload_n_deploy
import zip_n_unzip
import creating_kvm
import edit_spike_arrest_policy
import change_statistic_collector_policy


filename=""
current_path = ""
bearer_token =""

with open("config.json") as json_data_file:
    data = json.load(json_data_file)
current_path= data['path']
bearer_token =data['token']
org=data['org_name']
evn=data['environment']
count_of_resources=0

############################################ Upload and deploy Multiple Shared Flows #####################################
shareflows_folder_path=current_path+"\\sharedflows"
resource_type="sharedflows"
resource_id = "sharedflowId"
filenames = os.listdir(shareflows_folder_path)
for filename in filenames:
	filename =filename.strip()
	filename =re.search(r'(.*?).zip',filename)
	if filename:
		filename = str(filename.group(1))
		print(filename)
		count_of_resources=count_of_resources +1
		zip_n_unzip.Unzip.unzip_file(filename,shareflows_folder_path+"\\"+filename)
		zip_n_unzip.Zip.create_newzip_after_changes(filename,shareflows_folder_path)
		upload_zip=upload_n_deploy
		upload_n_deploy.Upload.upload_to_hybrid(shareflows_folder_path,filename,bearer_token,org,resource_type,resource_id)
		upload_n_deploy.Deploy.deploy_to_hybrid(evn,filename,bearer_token,org,resource_type)

print("==================================================")
print("| Completed uploading and Deploying Shared Flows |")
print("|                                                |")
print("| Starting to Create KVM                         |")
print("==================================================")
################################################## Creating KVM 's ########################################################
createkvm=creating_kvm
kvm_folder_path="kvm"
createkvm.Createkvm.createkvm(current_path,kvm_folder_path,bearer_token,org)
print("=================================================")
print("| Completed Creating KVM                         |")
print("|                                                |")
print("==================================================")

########################################## Editing spike arest policy ######################################################
#filenames =['demo_spike_arrest_8','demo_spike_arrest_4','demo_spike_arrest_5','demo_spike_arrest_6','demo_spike_arrest_7']
#for filename in filenames:
	#spike_arrest = edit_spike_arrest_policy
	#spike_arrest.Main_spike_arrest.call_spike_arrest(current_path,filename,bearer_token,2,"test")


########################################### Editing Statistic Collector Policy #############################################
#resource_type="apis"
#resource_id = "apiProxyId"
#filenames=['statistic_collector_9']
#for filename in filenames:
	#print(filename)
	#statistic_collector = change_statistic_collector_policy
	#statistic_collector.Main_static_collector.call_static_collector(current_path,filename,bearer_token,resource_type,resource_id)

################################################ Deploy multiple proxies at once ##############################################
proxies_folder_path=current_path+"\\proxies"
try:
	filenames = os.listdir(proxies_folder_path)
	resource_type="apis"
	resource_id = "apiProxyId"
	for filename in filenames:
		filename =filename.strip()
		filename =re.search(r'(.*?).zip',filename)
		if filename:
			count_of_resources=count_of_resources +1
			filename = str(filename.group(1))
			if count_of_resources <=50:
				print(filename)
				print("Total Resources Count "+str(count_of_resources))
				zip_n_unzip.Unzip.unzip_file(filename,proxies_folder_path+"\\"+filename)
				zip_n_unzip.Zip.create_newzip_after_changes(filename,proxies_folder_path)
				upload_zip=upload_n_deploy
				upload_zip.Upload.upload_to_hybrid(proxies_folder_path,filename,bearer_token,org,resource_type,resource_id)
				upload_zip.Deploy.deploy_to_hybrid(evn,filename,bearer_token,org,resource_type)

except IOError:
    print('File not found at the specified location in config.json file')
