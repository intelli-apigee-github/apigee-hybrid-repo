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
class Handling_Target_Servers:
	"""docstring for Handling_Target_Servers"""
	def __init__(self):
		super(Handling_Target_Servers, self).__init__()
	def create_target_server(current_path,filename):
		try:
			file_TS=open(current_path+"\\proxies"+"\\"+filename+"\\apiproxy\\targets\\default.xml",'r')
			lines_1=file_TS.readlines()
			for line_1 in lines_1:
				#print(line_1)
				matches_target_servers=re.match(r'\s*<Server name="(.*?)"',line_1)
				if matches_target_servers:
					found_target_servers=matches_target_servers.group(1)
					found_target_servers=found_target_servers.strip()
					ts_path=current_path+"\\targetservers"
					file_open_ts=open(ts_path+"\\"+found_target_servers)
					#print(ts_path+"\\"+found_target_servers)
					lines_2=file_open_ts.readlines()
					for line_2 in lines_2:
						#print(line_2)
						pass
					file_open_ts.close()	

			file_TS.close()		
		except 	OSError as e:
			print("Failed with:", e.strerror) # look what it says
	
