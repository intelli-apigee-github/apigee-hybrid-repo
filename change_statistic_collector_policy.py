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
import edit_spike_arrest_policy
import requests



class Edit_static_collector:
	"""docstring for Editing StaticCollector Policy"""
	def __init__(self):
		super(Edit_static_collector, self).__init__()


	def edit_static_collector(path,filename,token):
		#dc_var_name=""

		file_to_delete=""
		src_file = 'C:\\Users\\SANTOSH\\Desktop\\DataCapture.xml'
		dest_dir = path+"\\"+filename+"\\apiproxy\\policies"
		os.chdir(path+"\\"+filename+"\\apiproxy\\policies")
		arr = os.listdir()
		policy_name=''
		policy_display_name=''
		assigned_var=''
		referenced_var=''
		type_var=''
		for i in arr:
			print(i)
			file2=open(path+"\\"+filename+"\\apiproxy\\policies\\"+i, 'r')
			lines=file2.readlines()
			for line in lines:
				pattern = '<StatisticsCollector'
				result = re.match(pattern, line)
				if result:
					print("StatisticsCollector policy found and needs to be removed")
					print("Current File Name "+i)
					file_to_delete=i
					print("File to delete "+file_to_delete)
					print("Copying the required  Statistic Collector policy file")
					shutil.copy(src_file,dest_dir)
					print("Copied")
				match_name =re.search(r'<StatisticsCollector.*name="(.*?)"',line)
				if match_name:
					policy_name =match_name.group(1)
				match_display_name =re.search(r'<DisplayName>(.*?)</DisplayName>',line)
				if match_display_name:
					policy_display_name=match_display_name.group(1)
				match_variables =re.search(r'<Statistic name="(.*?)" ref="(.*?)" type="(.*?)"',line)
				if match_variables:
					assigned_var=match_variables.group(1)
					referenced_var=match_variables.group(2)
					type_var=match_variables.group(3)
				match_default_value =re.search(r'<Statistic .*>(.*?)</Statistic',line)
				if match_default_value:
					default_value_stats=match_default_value.group(1).strip()
				else:
					default_value_stats="0"
			file2.close()
		print("Deleting "+file_to_delete+" policy file")
		os.remove(path+"\\"+filename+"\\apiproxy\\policies\\"+file_to_delete)
		print("Successfully deleted StatisticsCollector policy ")
		match_dc_file_name=''
		os.chdir(path+"\\"+filename+"\\apiproxy\\policies")
		arr = os.listdir()
		for i in arr:
			file3=open(path+"\\"+filename+"\\apiproxy\\policies\\"+i, 'r')
			lines=file3.readlines()
			for line in lines:
				#print(line)
				pattern = '<DataCapture'
				result = re.match(pattern, line)
				if result:
					print("DataCapture policy found")
					match_dc_file_name=re.search(r'DataCapture.*name="(.*?)"',line)
					if match_dc_file_name:
						m_dc_file_name=match_dc_file_name.group(1)
				match_dc_var_name = re.search(r'<DataCollector>(.*?)</DataCollector>',line)
				if match_dc_var_name:
					dc_var_name = match_dc_var_name.group(1)
					print("DATA COLLECTOR VALUE : " +match_dc_var_name.group(1))
					dc_store_obj=Dc_store
					dc_store_obj.dc_store(token,dc_var_name)
					

			file3.close()
		print("Changing values inside the DataCapture policy to match with the Statistic Collector Policy")
		pyutil.filereplace(path+"\\"+filename+"\\apiproxy\\policies\\"+m_dc_file_name+'.xml','<DataCapture name="DataCapture"','<DataCapture name="'+policy_name+'"')
		pyutil.filereplace(path+"\\"+filename+"\\apiproxy\\policies\\"+m_dc_file_name+'.xml',' <DisplayName>DataCapturepolicy</DisplayName>',' <DisplayName>'+policy_display_name+'</DisplayName>')
		if default_value_stats == 0:
			pyutil.filereplace(path+"\\"+filename+"\\apiproxy\\policies\\"+m_dc_file_name+'.xml','<Collect ref="existing-variable" default="0"/>','<Collect ref="'+referenced_var+'" default="0"/>')
		else:
			pyutil.filereplace(path+"\\"+filename+"\\apiproxy\\policies\\"+m_dc_file_name+'.xml','<Collect ref="existing-variable" default="0"/>','<Collect ref="'+referenced_var+'" default="'+default_value_stats+'"/>')
			print("Changes Applied")
		print("Renaming the DataCapture Policy to match with Statistic Collector policy")
		os.rename(path+"\\"+filename+"\\apiproxy\\policies\\"+m_dc_file_name+'.xml', path+"\\"+filename+"\\apiproxy\\policies\\"+file_to_delete)
		print("Renamed")


class Dc_store:
	"""docstring for DCStore"""
	def __init__(self):
		super(dc_store).__init__()
	
	def dc_store(token,dc_var_name):
		url="https://apigee.googleapis.com/v1/organizations/apigee-hybrid-demo-305106/datacollectors"
		payload = "{\r\n  \"name\": \""+dc_var_name+"\",\r\n  \"description\": \"Collects data for analysis.\",\r\n  \"type\": \"STRING\",\r\n}"
		headers = {'Authorization' : 'Bearer '+token , 'Content-Type': 'text/plain'}
		response = requests.request("POST", url, headers=headers, data=payload)
		print(response.text)


		
		



class Main_static_collector:
	"""docstring for Main_static_collector"""
	def __init__(self):
		super(Main_static_collector, self).__init__()
	def call_static_collector(path,filename,token,resource_type,resource_id):
		e_static_collector=Edit_static_collector
		zu.Unzip.unzip_file(filename)
		e_static_collector.edit_static_collector(path,filename,token)
		zu.Zip.create_newzip_after_changes(filename,path)
		upload_zip=ud
		upload_zip.Upload.upload_to_hybrid(path,filename,token,resource_type,resource_id)
		upload_zip.Deploy.deploy_to_hybrid("test",filename,token,resource_type)
