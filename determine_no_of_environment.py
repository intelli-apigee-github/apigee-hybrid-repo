import sys
import os
from os import path
import re
import json
import pyutil

with open("config.json") as json_data_file:
    data = json.load(json_data_file)
    json_data_file.close()
current_path= data['path']

count=0
proxies_folder_path=current_path+"\\proxies"
filenames = os.listdir(proxies_folder_path)
for filename in filenames:
		filename =filename.strip()
		pattern=".zip"
		pat =re.search(r'\.(.*?)\s*',filename)
		if pat:
			count=count+1
print("--------------------------------------------------------------------------")			
print("|                      Total Proxies "+str(count)+"                                 |")
print("--------------------------------------------------------------------------")			

count_sf=0
proxies_folder_path=current_path+"\\sharedflows"
filenames = os.listdir(proxies_folder_path)
for filename in filenames:
		filename =filename.strip()
		pattern=".zip"
		pat =re.search(r'\.(.*?)\s*',filename)
		if pat:
			count_sf=count_sf+1
print("--------------------------------------------------------------------------")			
print("|                      Total sharedflows "+str(count_sf)+"    	        		 |")
print("--------------------------------------------------------------------------")			

print("--------------------------------------------------------------------------")			
print("|                      Total Environments  "+str(int(((count+count_sf)/50)+1))+"       		         |")
print("--------------------------------------------------------------------------")			

req_evn=int(((count+count_sf)/50)+1)
evn=[]
for i in range(0,req_evn):
	evn.append("test"+str(i))
print(str(evn))
evn=str(evn)
evn=evn.replace('\'','\"')

############# Update Config.json File ####################
pyutil.filereplace("config.json",'\\[.*\\]',evn)
