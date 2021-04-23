import sys
import os
import shutil
import zipfile as zp
import re
#from pyutil import filereplace
import json
import requests
import upload_n_deploy
import zip_n_unzip


class Createkvm:
	"""docstring for Createkvm"""
	def __init__(self):
		super(Createkvm).__init__()

	def createkvm(path,filename,token,org):
		rootdir = path +"\\"+filename
		for subdir, dirs, files in os.walk(rootdir):
			for file in files:
				cur_path=os.path.join(subdir, file)
				if(file != "privacy"):
					#print("KVM  "+file +" Created ")
					match_evn=re.search(r'env\\(.*?)\\',cur_path)
					if match_evn:
						env=match_evn.group(1)
						url = "https://apigee.googleapis.com/v1/organizations/"+org+"/environments/"+env+"/keyvaluemaps"
						payload = "{\r\n  \"encrypted\": true,\r\n  \"name\": \""+file+"\"\r\n}"
						headers = {'Authorization': 'Bearer '+token,'Content-Type': 'text/plain'}
						response = requests.request("POST", url, headers=headers, data=payload)
						#print(response.text)
						status_code = response.status_code
						if(status_code !=201):
							print("-------------------------------------------------------------------------------------------")
							print("|                         Error while creating "+file+" KVM                                ")
							print("-------------------------------------------------------------------------------------------")

							print(response.text)
							
						else:
							#print(response.text)
							print("-------------------------------------------------------------------------------------------")
							print("|   KVM  " +file+" created in " +env+ " environment")
							print("-------------------------------------------------------------------------------------------")
	



#createkvm=Createkvm
#createkvm.createkvm(current_path,filename,bearer_token)

















		






	


			

