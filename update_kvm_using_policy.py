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
	def  update_kvm_using_policy(path,filename,token,org):
		rootdir = path +"\\"+filename
		for subdir, dirs, files in os.walk(rootdir):
			for file in files:
				cur_path=os.path.join(subdir, file)
				if(file != "privacy"):
					print("KVM Files  "+file)
					file_kvm_files=open('C:\\Users\\SANTOSH\\Desktop\\Apigee\\python-apigeetool\\data\\kvm\\env\\test\\'+file, 'r')
					lines=file_kvm_files.readlines()
					for line in lines:
						print(line)
						match_kvm_name=re.search(r' "value" : "(.*?)"',line)
						if match_kvm_name:
							print(match_kvm_name.group(1))


					file_kvm_files.close()
	def read_kvm_file():
		try:
			
			kvm_names = os.listdir("C:\\Users\\SANTOSH\\Desktop\\Apigee\\python-apigeetool\\data\\kvm\\env\\test")
			print(kvm_names)
			tota_kvm=len(kvm_names)
			list_of_kvm_values=[]
			q=''
			#count=0
			#for kvm_name in kvm_names:
				#with open('C:\\Users\\SANTOSH\\Desktop\\Apigee\\python-apigeetool\\data\\kvm\\env\\test\\'+kvm_name) as json_data_file:
					#data = json.load(json_data_file)
					#json_data_file.close()
				#q=q+data['name']+","+str(data['encrypted'])+","
				#list_of_kvm_values.append(data['name'])
				#list_of_kvm_values.append(data['encrypted'])
				#values =data['entry']
				#for value in values:
					#list_of_kvm_values.append(value['name'])
					#list_of_kvm_values.append(value['value'])
					#q=q+"["+value['name']+"],["+value['value']+"]," 	
				#q=q+"\n"
			#print(q)		
		except OSError as e:
			print(e.strerror)


							
		print(list_of_kvm_values)			