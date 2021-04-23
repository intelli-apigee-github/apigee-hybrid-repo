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
class Edit_Spike_Arrest:
	"""docstring for Edit_Spike_Arrest"""
	def __init__(self):
		super(Edit_Spike_Arrest, self).__init__()
	def edit_spike_arrest(current_path,proxy_name_include_sa,name_sa,token,no_of_mp):

		ref_var =''
		value_of_effective_count='false'
		file_spike_arrest=open(current_path+"\\proxies"+"\\"+proxy_name_include_sa+"\\apiproxy\\policies"+"\\"+name_sa+".xml", 'r')
		lines=file_spike_arrest.readlines()
		for line in lines:
			#print(line)
			match_spike_1=re.search(r'<Rate ref="(.*?)"/>',line)
			if match_spike_1:
				ref_var=match_spike_1.group(1)
				#print("Reference variable value is ====>"+ref_var)


			match_spike_2 = re.search( r"<Rate>(.*?)</Rate>", line)
			if match_spike_2:
				#print(match_spike_2.group(1))
				original_spike_rate=match_spike_2.group(1)
				match_only_digit = re.search(r"(.*?)p",original_spike_rate)
				if match_only_digit:
					#print(match_only_digit.group(1))
					only_digit = match_only_digit.group(1)
				match_unit = re.search(r"p(.*)",original_spike_rate)
				if match_unit:
					#print(match_unit.group(1))
					unit_spike=match_unit.group(1)	
			matches_true=re.search(r"\s*<UseEffectiveCount>(.*?)</UseEffectiveCount>",line)
			if (matches_true):
				
				value_of_effective_count = matches_true.group(1)
				#print(value_of_effective_count)
				#print(matches_true.group(1))
			if  ref_var !="":
				print("--------------------------------------------------------------------------------------------")
				print("|            Spike Arrest Rate is Configured From KVM please update KVM                    |")	
				print("--------------------------------------------------------------------------------------------")


			if (value_of_effective_count == "true") & (ref_var == ""):
				changed_spike_rate=no_of_mp*int(only_digit)
				#print("Changed Spike rate "+str(changed_spike_rate))
				#print(current_path+"\\proxies"+"\\"+proxy_name_include_sa+"\\apiproxy\\policies\\"+name_sa+".xml")
				pyutil.filereplace(current_path+"\\proxies"+"\\"+proxy_name_include_sa+"\\apiproxy\\policies\\"+name_sa+".xml","<UseEffectiveCount>true</UseEffectiveCount>","")
				pyutil.filereplace(current_path+"\\proxies"+"\\"+proxy_name_include_sa+"\\apiproxy\\policies\\"+name_sa+".xml","<Rate>"+original_spike_rate+"</Rate>","<Rate>"+str(changed_spike_rate)+"p"+unit_spike+"</Rate>")
				
		file_spike_arrest.close()	
			

