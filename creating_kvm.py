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
import edit_spike_arrest_policy
import change_statistic_collector_policy


#filename="kvm"
#env=""
#bearer_token="ya29.a0AfH6SMDjJfitSOYK_LXvyr-ctPr6g6cTIy_Gjvx7nuJSnPArog0sb7ESd4MdANuzN81_u_iK5iajYGliJLaHG0jqB43Mqor8Tpne3LDc3AVolP4aIrkMh_Bj8luEKRZUwCIDfyaSaWkJfGMaXZl8EhWg1dNxC0Z2RN6zogZBtooLhD776MoYSbtOhhXTfPlrS-tp4PKYN_2N8Vw20701kAvov9Inqknc_ZHv4Nm1Dju_AniHH_qwTYv16mGRZvodfwKBiGI"
#current_path = os.path.dirname(os.path.realpath(__file__))

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
						print("KVM  " +file+" created in " +env+ " environment")
						url = "https://apigee.googleapis.com/v1/organizations/"+org+"/environments/"+env+"/keyvaluemaps"
						payload = "{\r\n  \"encrypted\": true,\r\n  \"name\": \""+file+"\"\r\n}"
						headers = {'Authorization': 'Bearer '+token,'Content-Type': 'text/plain'}
						response = requests.request("POST", url, headers=headers, data=payload)
						#print(response.text)
						status_code = response.status_code
						if(status_code !=201):
							print("Error while Creating KVM")
							print(response.text)
							exit()
						else:
							print(response.text)	



#createkvm=Createkvm
#createkvm.createkvm(current_path,filename,bearer_token)

















		






	


			

