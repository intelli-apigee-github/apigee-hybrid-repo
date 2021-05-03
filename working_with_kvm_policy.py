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
from update_kvm_using_policy import Update_KVM

filename=""
current_path = ""
bearer_token =""

with open("config.json") as json_data_file:
    data = json.load(json_data_file)
    json_data_file.close()
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

os.chdir(proxies_folder_path)
#filenames = os.listdir(proxies_folder_path)
#print(filenames)
filenames=['create_kvm_rec1.zip']


for filename in filenames:
	filename =filename.strip()
	if filename:
		filename =re.search(r'(.*?).zip',filename)
		filename = str(filename.group(1))
		zip_n_unzip.Unzip.unzip_file(filename,current_path+"\\proxies"+"\\"+filename)
		os.chdir(current_path+"\\proxies"+"\\"+filename+"\\apiproxy\\policies\\")
		arr = os.listdir()
		for i in arr:
			file2=open(current_path+"\\proxies"+"\\"+filename+"\\apiproxy\\policies"+"\\"+i, 'r')
			lines=file2.readlines()
			for line in lines:
				print(line)
				kvm_check = re.search(r'\s*<SharedFlowBundle>(.*?)</SharedFlowBundle>',line)

