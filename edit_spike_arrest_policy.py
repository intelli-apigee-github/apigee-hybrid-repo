import sys
import os
import re
import pyutil
#import filereplace
import upload_n_deploy as ud
import zip_n_unzip as zu


class Edit_spike_arrest:
	"""docstring for ClassName"""
	def __init__(self):
		super(Edit_spike_arrest, self).__init__()

	def edit_spike_arrest(path,filename,no_of_mp,token):
		file_to_delete=""
		#message_processor =2
		os.chdir(path+"\\"+filename+"\\apiproxy\\policies")
		original_spike_rate=0
		arr = os.listdir()
		print(arr)
		ref_var=""
		for i in arr:
			file2=open(path+"\\"+filename+"\\apiproxy\\policies\\"+i, 'r')
			lines=file2.readlines()
			print(lines)
			for line in lines:
				print(line)
				pattern = '<SpikeArrest'
				result = re.match(pattern, line)
				if result:
					print("Editing Spike Arrest policy")
					print("Current File Name "+i)
					file_to_delete=i
					print("Display Name Of Spike Arrest Policy"+file_to_delete)
					#exit()
				match = re.search( r"<Rate(.*?)>(.*?)</Rate>", line)
				if match:
					print(match.group(1))
					#exit()
					reference_var=match.group(1)
					if reference_var != "":
						print("Spike Arrest rate is referenced from KVM /Request")
						ref_var=reference_var
					else:
						print("Spike Arrest rate is defined inline")
						ref_var=reference_var
						original_spike_rate = match.group(2)
						print(original_spike_rate)
					match_only_digit = re.search(r"(.*?)p",original_spike_rate)
					if match_only_digit:
						print(match_only_digit.group(1))
						only_digit = match_only_digit.group(1)
					match_unit = re.search(r"p(.*)",original_spike_rate)
					if match_unit:
						print(match_unit.group(1))
						unit_spike=match_unit.group(1)
				matches_true=re.search(r"<UseEffectiveCount>(.*?)</UseEffectiveCount?",line)
				if (matches_true):
					value_of_effective_count = matches_true.group(1).strip()
					print(value_of_effective_count)
					print(matches_true.group(1))
					if  ref_var !="":
						print("The Spike Arrest Rate is Configured From KVM please update KVM")
					if (value_of_effective_count == "true") & (ref_var == ""):
						changed_spike_rate=no_of_mp*int(only_digit)
						print(changed_spike_rate)
						pyutil.files.filereplace(path+"\\"+filename+"\\apiproxy\\policies\\"+file_to_delete,"<UseEffectiveCount>true</UseEffectiveCount>","")
						pyutil.files.filereplace(path+"\\"+filename+"\\apiproxy\\policies\\"+file_to_delete,"<Rate>"+original_spike_rate+"</Rate>","<Rate>"+str(changed_spike_rate)+"p"+unit_spike+"</Rate>")
					else:
						pyutil.files.filereplace(path+"\\"+filename+"\\apiproxy\\policies\\"+file_to_delete,"<UseEffectiveCount>false</UseEffectiveCount>","")
			file2.close()

class Main_spike_arrest:
	"""docstring for ClassName"""
	def __init__(self):
		super(Main_spike_arrest, self).__init__()
	
	def call_spike_arrest(path,filename,token,no_of_mp,evn):
		e_spike_arrest =Edit_spike_arrest
		zu.Unzip.unzip_file(filename)
		e_spike_arrest.edit_spike_arrest(path,filename,no_of_mp,token)
		zu.Zip.create_newzip_after_changes(filename,path)
		upload_zip=ud
		upload_zip.Upload.upload_to_hybrid(path,filename,token,resource_type,resource_id)
		upload_zip.Deploy.deploy_to_hybrid("test",filename,token,resource_type)





		

