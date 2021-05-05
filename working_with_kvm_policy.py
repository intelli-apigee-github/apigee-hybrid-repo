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

filenames=['create_kvm_values_demo.zip']
filename="create_kvm_values_demo"
zip_n_unzip.Unzip.unzip_file(filename,current_path+"\\proxies"+"\\"+filename)

try:
	
	kvm_names = os.listdir("C:\\Users\\SANTOSH\\Desktop\\Apigee\\python-apigeetool\\data\\kvm\\env\\test")
	#print(kvm_names)
	print("------------------------------------------------------")	
	print("|  Total KVM,s " +str(len(kvm_names)))
	print("------------------------------------------------------")


	print("------------------------------------------------------")
	print("| Copying the required KVM DUMMY  policy file     |")
	print("------------------------------------------------------")

	src_file = 'C:\\Users\\SANTOSH\\Desktop\\KVM.xml'
	dest_dir = current_path+"\\proxies"+"\\create_kvm_values_demo\\apiproxy\\policies"
	shutil.copy(src_file,dest_dir)
	print("------------------------------------------------------")
	print("|                   Copied                           |")	
	print("------------------------------------------------------")	


	tota_kvm=len(kvm_names)
	list_of_kvm_values=[]
	q=''
	count=0
	steps_variable =""
	policy_variable=''
	manifest_variable =''

	for kvm_name in kvm_names:
		with open('C:\\Users\\SANTOSH\\Desktop\\Apigee\\python-apigeetool\\data\\kvm\\env\\test\\'+kvm_name) as json_data_file:
			data = json.load(json_data_file)
			json_data_file.close()

		print("KVM MAP IDENTIFIER "+kvm_name)
		os.rename(current_path+"\\proxies"+"\\create_kvm_values_demo\\apiproxy\\policies\\KVM.xml", current_path+"\\proxies"+"\\create_kvm_values_demo\\apiproxy\\policies\\kvm_"+kvm_name+".xml")
		print("------------------------------------------------------")
		print("|                 Renamed                            |")		
		print("------------------------------------------------------")
		
		################################ Replacing Variable inside the KVM File ############################################
		pyutil.filereplace(current_path+"\\proxies"+"\\create_kvm_values_demo\\apiproxy\\policies\\kvm_"+kvm_name+'.xml','mapIdentifier="Basic-Auth"','mapIdentifier="'+kvm_name+'"')
		pyutil.filereplace(current_path+"\\proxies"+"\\create_kvm_values_demo\\apiproxy\\policies\\kvm_"+kvm_name+'.xml','name="KVM_dummy"','name="kvm_'+kvm_name+'"')
		pyutil.filereplace(current_path+"\\proxies"+"\\create_kvm_values_demo\\apiproxy\\policies\\kvm_"+kvm_name+'.xml','<DisplayName>KVM</DisplayName>','<DisplayName>kvm_'+kvm_name+'</DisplayName>')

		q=q+data['name']+","+str(data['encrypted'])+","
		list_of_kvm_values.append(data['name'])
		list_of_kvm_values.append(data['encrypted'])
		
		values =data['entry']
		for value in values:
			list_of_kvm_values.append(value['name'])
			list_of_kvm_values.append(value['value'])
			

			q=q+"|*  ["+value['name']+"],["+value['value']+"]  *| " 	
		q=q+"\n"
		#print(q)
		matches_key_val=re.search(r''+kvm_name+'.*\\[(.*?)\\]',q)
		if matches_key_val:
			key_values=matches_key_val.group(0)
			splited_values = key_values.split("|*")
			#print(len(splited_values))
			length_of_kv=len(splited_values)
			add_multiple_kv=''
			for kvm in range(0,length_of_kv):
				if kvm ==0:
					continue 
				#print(splited_values[kvm])
				extract_key_values=re.search(r'\[(.*?)\]\,\[(.*?)\]',splited_values[kvm])
				if extract_key_values:
					print("Keys ====>" +extract_key_values.group(1))
					indivi_key=extract_key_values.group(1)
					print("Values  ====>" +extract_key_values.group(2))
					indivi_value= extract_key_values.group(2)
					add_multiple_kv=add_multiple_kv+"<Key><Parameter>"+indivi_key+"</Parameter></Key><Value>"+indivi_value+"</Value>"
					#print(add_multiple_kv)
			pyutil.filereplace(current_path+"\\proxies"+"\\create_kvm_values_demo\\apiproxy\\policies\\kvm_"+kvm_name+'.xml','<Key>\\s*<Parameter>password2\\s*</Parameter>\\s*</Key>\\s*<Value>justsecret\\s*</Value>',add_multiple_kv)


		print("------------------------------------------------------")
		print("| Copying the required KVM DUMMY policy file         |")
		print("------------------------------------------------------")
		src_kvm_file = 'C:\\Users\\SANTOSH\\Desktop\\KVM.xml'
		dest_kvm_dir = current_path+"\\proxies"+"\\create_kvm_values_demo\\apiproxy\\policies"
		shutil.copy(src_kvm_file,dest_kvm_dir)
		print("------------------------------------------------------")
		print("|                   Copied                           |")	
		print("------------------------------------------------------")
		steps_variable =steps_variable+"<Step><Name>kvm_"+kvm_name+"</Name></Step>"
		policy_variable=policy_variable+" <Policy>kvm_"+kvm_name+"</Policy>"	
		manifest_variable=manifest_variable +"<VersionInfo resourceName= 'kvm_"+kvm_name+"' version='SHA-512:3875e5b9dad448c08921966e7bdc459cb19b774ee9701700821365d330d551e5b7639817879cb31ad7853165e3b60707d05f3b4d0ee2028cc005e940c4700556'/>"
		#print(q)
	#print(steps_variable)
	############################################ Replacing Steps in default xml ################################################
	pyutil.filereplace(current_path+"\\proxies"+"\\create_kvm_values_demo\\apiproxy\\proxies\\default.xml",'\\s*<Step>\\s*<Name>\\s*KVM_DUMMY\\s*</Name>\\s*</Step>','<Step><Name>KVM_DUMMY</Name></Step>'+steps_variable)

	############################################ Replacing Policies in Root Folder ################################################	
	pyutil.filereplace(current_path+"\\proxies"+"\\create_kvm_values_demo\\apiproxy\\create_kvm_values.xml",'\\s*<Policy>KVM_DUMMY</Policy>','<Policy>KVM_DUMMY</Policy>'+policy_variable)
			
	############################################ Replacing Policies in Manifest File ################################################	
	pyutil.filereplace(current_path+"\\proxies"+"\\create_kvm_values_demo\\apiproxy\\manifests\\manifest.xml",'\\s*<VersionInfo\\s*resourceName="KVM_DUMMY"\\s*version="SHA-512:3875e5b9dad448c08921966e7bdc459cb19b774ee9701700821365d330d551e5b7639817879cb31ad7853165e3b60707d05f3b4d0ee2028cc005e940c4700556"/>','<VersionInfo resourceName="KVM_DUMMY" version="SHA-512:3875e5b9dad448c08921966e7bdc459cb19b774ee9701700821365d330d551e5b7639817879cb31ad7853165e3b60707d05f3b4d0ee2028cc005e940c4700556"/>'+manifest_variable)

	######################################### Disable the DUMMY Policy ###############################################################
	pyutil.filereplace(current_path+"\\proxies"+"\\create_kvm_values_demo\\apiproxy\\policies\\KVM_DUMMY.xml",'enabled="true"','enabled="false"')

	resource_type="apis"
	resource_id = "apiProxyId"
	zip_n_unzip.Zip.create_newzip_after_changes("create_kvm_values_demo",current_path+"\\proxies")

except OSError as e:
	print(e.strerror)
