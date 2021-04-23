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
class Edit_Statistic_Collector:
	"""docstring for Edit_Statistic_Collector"""
	def __init__(self):
		super(Edit_Statistic_Collector, self).__init__()
		
	def edit_statistic_collector(current_path,proxy_name_include_sc,name_sc,token,src_dc_file):
		referenced_var =''
		file_statistic_collector=open(current_path+"\\proxies"+"\\"+proxy_name_include_sc+"\\apiproxy\\policies"+"\\"+name_sc+".xml", 'r')
		lines=file_statistic_collector.readlines()
		for line in lines:
			match_ref_variable =re.search(r'\s*<Statistic.*ref="(.*?)"',line)
			if match_ref_variable:
				referenced_var=match_ref_variable.group(1)
				#print("<========================= Value of Referenced Var ======================>"+referenced_var)
			match_display_name =re.search(r'<DisplayName>(.*?)</DisplayName>',line)
			if match_display_name:
				policy_display_name=match_display_name.group(1)
			match_default_value =re.search(r'<Statistic .*>(.*?)</Statistic',line)
			if match_default_value:
				default_value_stats=match_default_value.group(1).strip()	
			else:
				default_value_stats="0"
		file_statistic_collector.close()
		print("------------------------------------------------------")
		print("| Copying the required Data Capture  policy file     |")
		print("------------------------------------------------------")

		#src_file = 'C:\\Users\\SANTOSH\\Desktop\\DataCapture.xml'
		dest_dir = current_path+"\\proxies"+"\\"+proxy_name_include_sc+"\\apiproxy\\policies"
		shutil.copy(src_dc_file,dest_dir)
		print("------------------------------------------------------")
		print("|                   Copied                           |")	
		print("------------------------------------------------------")



		file_data_capture=open(current_path+"\\proxies"+"\\"+proxy_name_include_sc+"\\apiproxy\\policies"+"\\DataCapture.xml", 'r')
		lines =file_data_capture.readlines()
		for line in lines:
			#print(line)
			match_dc_file_name=re.search(r'DataCapture.*name="(.*?)"',line)
			if match_dc_file_name:
				m_dc_file_name=match_dc_file_name.group(1)
				#print(m_dc_file_name)	
			match_dc_var_name = re.search(r'<DataCollector>(.*?)</DataCollector>',line)
			if match_dc_var_name:
				dc_var_name = match_dc_var_name.group(1)
				#print(dc_var_name)
				print("DATA COLLECTOR VALUE : " +match_dc_var_name.group(1))
				dc_store_obj=Dc_store
				dc_store_obj.dc_store(token,dc_var_name)	
		file_data_capture.close()	


		pyutil.filereplace(current_path+"\\proxies"+"\\"+proxy_name_include_sc+"\\apiproxy\\policies\\"+m_dc_file_name+'.xml','<DataCapture name="DataCapture"','<DataCapture name="'+name_sc+'"')
		pyutil.files.filereplace(current_path+"\\proxies"+"\\"+proxy_name_include_sc+"\\apiproxy\\policies\\"+m_dc_file_name+'.xml',' <DisplayName>DataCapturepolicy</DisplayName>',' <DisplayName>'+policy_display_name+'</DisplayName>')
		if default_value_stats == 0:
			pyutil.files.filereplace(current_path+"\\proxies"+"\\"+proxy_name_include_sc+"\\apiproxy\\policies\\"+m_dc_file_name+'.xml','<Collect ref="existing-variable" default="0"/>','<Collect ref="'+referenced_var+'" default="0"/>')
		else:
			pyutil.files.filereplace(current_path+"\\proxies"+"\\"+proxy_name_include_sc+"\\apiproxy\\policies\\"+m_dc_file_name+'.xml','<Collect ref="existing-variable" default="0"/>','<Collect ref="'+referenced_var+'" default="'+default_value_stats+'"/>')
			print("------------------------------------------------------")
			print("|             Changes Applied                        |")
			print("------------------------------------------------------")


		
		os.remove(current_path+"\\proxies"+"\\"+proxy_name_include_sc+"\\apiproxy\\policies\\"+name_sc+".xml")
		print("------------------------------------------------------")
		print("!  Successfully deleted StatisticsCollector policy   |")
		print("------------------------------------------------------")
		#print(m_dc_file_name)
		print("------------------------------------------------------")
		print("!        Renaming the DataCapture Policy             |")
		print("------------------------------------------------------")
	
		os.rename(current_path+"\\proxies"+"\\"+proxy_name_include_sc+"\\apiproxy\\policies\\"+m_dc_file_name+'.xml', current_path+"\\proxies"+"\\"+proxy_name_include_sc+"\\apiproxy\\policies\\"+name_sc+".xml")
		print("------------------------------------------------------")
		print("|                 Renamed                            |")		
		print("------------------------------------------------------")
