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
class Update_KVM:
	"""docstring for Update_KVM"""
	def __init__(self):
		super(Update_KVM, self).__init__()
	def  update_kvm_using_policy(current_path,src_kvm_file):
		try:
			proxies_folder_path=current_path+"\\proxies"
			os.chdir(proxies_folder_path)
			filenames=['create_kvm_values_demo.zip']
			filename="create_kvm_values_demo"
			zip_n_unzip.Unzip.unzip_file(filename,current_path+"\\proxies"+"\\"+filename)
			kvm_names = os.listdir(current_path+"\\kvm\\env\\test")
			#print(kvm_names)
			print("------------------------------------------------------")	
			print("|  Total KVM,s " +str(len(kvm_names)))
			print("------------------------------------------------------")
			print("------------------------------------------------------")
			print("| Copying the required KVM DUMMY  policy file     |")
			print("------------------------------------------------------")
			dest_kvm_dir = current_path+"\\proxies"+"\\"+filename+"\\apiproxy\\policies"
			shutil.copy(src_kvm_file,dest_kvm_dir)
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
				with open(current_path+ '\\kvm\\env\\test\\'+kvm_name) as json_data_file:
					data = json.load(json_data_file)
					json_data_file.close()

				print("KVM MAP IDENTIFIER "+kvm_name)
				os.rename(current_path+"\\proxies"+"\\"+filename+"\\apiproxy\\policies\\KVM.xml", current_path+"\\proxies"+"\\create_kvm_values_demo\\apiproxy\\policies\\kvm_"+kvm_name+".xml")
				print("------------------------------------------------------")
				print("|                 Renamed                            |")		
				print("------------------------------------------------------")
				
				################################ Replacing Variable inside the KVM File ############################################
				pyutil.filereplace(current_path+"\\proxies"+"\\"+filename+"\\apiproxy\\policies\\kvm_"+kvm_name+'.xml','mapIdentifier="Basic-Auth"','mapIdentifier="'+kvm_name+'"')
				pyutil.filereplace(current_path+"\\proxies"+"\\"+filename+"\\apiproxy\\policies\\kvm_"+kvm_name+'.xml','name="KVM_dummy"','name="kvm_'+kvm_name+'"')
				pyutil.filereplace(current_path+"\\proxies"+"\\"+filename+"\\apiproxy\\policies\\kvm_"+kvm_name+'.xml','<DisplayName>KVM</DisplayName>','<DisplayName>kvm_'+kvm_name+'</DisplayName>')

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
				dest_kvm_dir = current_path+"\\proxies"+"\\"+filename+"\\apiproxy\\policies"
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
			pyutil.filereplace(current_path+"\\proxies"+"\\"+filename+"\\apiproxy\\proxies\\default.xml",'\\s*<Step>\\s*<Name>\\s*KVM_DUMMY\\s*</Name>\\s*</Step>','<Step><Name>KVM_DUMMY</Name></Step>'+steps_variable)

			############################################ Replacing Policies in Root Folder ################################################	
			pyutil.filereplace(current_path+"\\proxies"+"\\"+filename+"\\apiproxy\\create_kvm_values.xml",'\\s*<Policy>KVM_DUMMY</Policy>','<Policy>KVM_DUMMY</Policy>'+policy_variable)
					
			############################################ Replacing Policies in Manifest File ################################################	
			pyutil.filereplace(current_path+"\\proxies"+"\\"+filename+"\\apiproxy\\manifests\\manifest.xml",'\\s*<VersionInfo\\s*resourceName="KVM_DUMMY"\\s*version="SHA-512:3875e5b9dad448c08921966e7bdc459cb19b774ee9701700821365d330d551e5b7639817879cb31ad7853165e3b60707d05f3b4d0ee2028cc005e940c4700556"/>','<VersionInfo resourceName="KVM_DUMMY" version="SHA-512:3875e5b9dad448c08921966e7bdc459cb19b774ee9701700821365d330d551e5b7639817879cb31ad7853165e3b60707d05f3b4d0ee2028cc005e940c4700556"/>'+manifest_variable)

			######################################### Disable the DUMMY Policy ###############################################################
			pyutil.filereplace(current_path+"\\proxies"+"\\"+filename+"\\apiproxy\\policies\\KVM_DUMMY.xml",'enabled="true"','enabled="false"')

			resource_type="apis"
			resource_id = "apiProxyId"
			zip_n_unzip.Zip.create_newzip_after_changes("create_kvm_values_demo",current_path+"\\proxies")
			print("Deploy and run create_kvm_values_demo  proxy to update all KVM values")

		except OSError as e:
			print(e.strerror)
			print(" create_kvm_values_demo.zip file is not found in the DATA Folder COPY the zip and try again ")
		
