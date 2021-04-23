import sys
import os
import shutil
import zipfile as zp
import re
#from pyutil import filereplace
import pyutil
import json
import requests
import upload_n_deploy  as ud
import zip_n_unzip as zu
import requests


class Dc_store:
	"""docstring for DCStore"""
	def __init__(self):
		super(dc_store).__init__()
	
	def dc_store(token,dc_var_name):
		url="https://apigee.googleapis.com/v1/organizations/apigee-hybrid-demo-305106/datacollectors"
		payload = "{\r\n  \"name\": \""+dc_var_name+"\",\r\n  \"description\": \"Collects data for analysis.\",\r\n  \"type\": \"STRING\",\r\n}"
		headers = {'Authorization' : 'Bearer '+token , 'Content-Type': 'text/plain'}
		response = requests.request("POST", url, headers=headers, data=payload)
		status_code = response.status_code
		print(response.text)
		if status_code == 401:
			print("--------------------------------------------------------------------------------------------")
			print("|                       !!! ERROR UNAUTHORIZED While Creating DC Store!!!                  |")
			print("--------------------------------------------------------------------------------------------")

			print(response.text)
			#exit()
		if status_code == 400:
			print("--------------------------------------------------------------------------------------------")
			print("   					  !!! ERROR The Zip Bundle Contains Error !!!                         |")
			print("--------------------------------------------------------------------------------------------")

			print(response.text)


