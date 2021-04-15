import sys
import os
import shutil
import zipfile as zp
import re
import pyutil
import filereplace
import json
import requests
import upload_n_deploy
import zip_n_unzip
import edit_spike_arrest_policy
import change_statistic_collector_policy


filename="backend-credentials"

current_path = os.path.dirname(os.path.realpath(__file__))
print(current_path)
bearer_token ="ya29.a0AfH6SMAGILwb98O-Oy9NgXfMZtKosbN69quD3Y36ORlKHGAK8myoXnuQLCUBondCNHmBCrLPnW4xkgx-b3lStbmRNWyy-wSfyiUIz5DUsC44AMJxjC3gr03UUU5vWI8KISDtP5VsMefeYwyPCJU6aecZeZGxNuolQkrKAvOI28oB5gXO6C7nlWgBJq54u3gXn6MnO1lc8KNLGaHKh8Yj1Qx1torG1opj6jI4WtckvfSzGwtI38COzMZkuU3JQjHl4AVeag"


############################################ Upload and deploy Multiple Shared Flows #####################################
#shareflows=["SF-quota"]
#resource_type="sharedflows"
#resource_id = "sharedflowId"
#for filename in shareflows:
	#zip_n_unzip.Unzip.unzip_file(filename)
	#zip_n_unzip.Zip.create_newzip_after_changes(filename,current_path)
	#upload_zip=upload_n_deploy
	#upload_n_deploy.Upload.upload_to_hybrid(current_path,filename,bearer_token,resource_type,resource_id)
	#upload_n_deploy.Deploy.deploy_to_hybrid("test",filename,bearer_token,resource_type)


################################################## Creating KVM 's ########################################################


########################################## Editing spike arest policy ######################################################
#filenames =['demo_spike_arrest_8','demo_spike_arrest_4','demo_spike_arrest_5','demo_spike_arrest_6','demo_spike_arrest_7']
#for filename in filenames:
	#spike_arrest = edit_spike_arrest_policy
	#spike_arrest.Main_spike_arrest.call_spike_arrest(current_path,filename,bearer_token,2,"test")


########################################### Editing Statistic Collector Policy #############################################
#resource_type="apis"
#resource_id = "apiProxyId"
#filenames=['statistic_collector_9']
#for filename in filenames:
	#print(filename)
	#statistic_collector = change_statistic_collector_policy
	#statistic_collector.Main_static_collector.call_static_collector(current_path,filename,bearer_token,resource_type,resource_id)

################################################ Deploy multiple proxies at once ##############################################
#list = [
		#"access_control_demo","accu-my-account","accuweather","AM-Add-Set","AM-copy-demo","AM-demo1",
		#"AM-new_req_obj","AM-prac_apikey","AM-remove-demo","BA-auth-demo","cache-demo","client_crentials_demo",
		#"condition-demo","cors-demo","cors-demo2","cors-demo3","cors-demo44","cors-enabled",
		#"CP-concurrent-demo","demo_populate_cache","DF-demo","edgemicro_hellojson","eight_demo_apigee","EV-demo1",
		#"EV-MV-demo","EV-uri","final_flow","first_demo_apigee","flows_demo","fourth_demo_apigee",
		#"FR_Execution_order","FR-custom","generate_oauth_userapi","getstarted","hello-hosted-targets","HT-demo",
		#"JSON-TP-demo","JS-raise_error","JS-sum_demo","JS-url-concat","JWT-demo","Jwt-demo1",
		#"JWT-verify","KVM-cache-demo","KVM-encrypted-demo","KVM-get-demo","KVM-update-insert","lab2a-v1",
		#"lab3a-v1","lab5a-v1","lab6a-v1","lab8a-v1","LB-Demo","Login-API",
		#"login-ro-api-prac","mock","mock2","mul_PE_Ep","mul_pe_te","multi_proxy_enpoints"

#]

#list = ["fourth_demo_apigee"]
resource_type="apis"
resource_id = "apiProxyId"
list =["fourth_demo_apigee"]
for filename in list:
	zip_n_unzip.Unzip.unzip_file(filename)
	zip_n_unzip.Zip.create_newzip_after_changes(filename,current_path)
	upload_zip=upload_n_deploy
	upload_zip.Upload.upload_to_hybrid(current_path,filename,bearer_token,resource_type,resource_id)
	upload_zip.Deploy.deploy_to_hybrid("test1",filename,bearer_token,resource_type)





