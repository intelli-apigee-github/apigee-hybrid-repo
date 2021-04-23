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
class Edit_Message_Logging:
	"""docstring for Edit_Message_Logging"""
	def __init__(self):
		super(Edit_Message_Logging, self).__init__()
		
	def edit_message_logging(current_path,proxy_name_include_ml,name_ml,token,message_log,host,port):
		file_message_logging=open(current_path+"\\proxies"+"\\"+proxy_name_include_ml+"\\apiproxy\\policies"+"\\"+name_ml+".xml", 'r')
		lines=file_message_logging.readlines()
		for line in lines:
			#print(line)
			matches_message_ml = re.match(r'\s*<Message>(.*?)</Message>',line)	
			if matches_message_ml:
				message_ml=matches_message_ml.group(1)
			matches_host_ml=re.match(r'\s*<Host>(.*?)</Host>',line)	
			if matches_host_ml:
				host_ml=matches_host_ml.group(1)
			matches_port_ml=re.match(r'\s*<Port>(.*?)</Port>',line)
			if matches_port_ml:
				port_ml=matches_port_ml.group(1)
				
		file_message_logging.close()

		pyutil.filereplace(current_path+"\\proxies"+"\\"+proxy_name_include_ml+"\\apiproxy\\policies\\"+name_ml+".xml","<Message>"+message_ml+"</Message>","<Message>"+message_log+"</Message>")
		pyutil.filereplace(current_path+"\\proxies"+"\\"+proxy_name_include_ml+"\\apiproxy\\policies\\"+name_ml+".xml","<Host>"+host_ml+"</Host>","<Host>"+host+"</Host>")
		pyutil.filereplace(current_path+"\\proxies"+"\\"+proxy_name_include_ml+"\\apiproxy\\policies\\"+name_ml+".xml","<Port>"+port_ml+"</Port>","<Port>"+port+"</Port>")
			
