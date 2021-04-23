import json
import requests



class Upload:
	"""This class uploads the zip to hybrid"""
	def __init__(self):
		super(Upload, self).__init__()
		
	
	def upload_to_hybrid(path,filename,token,org,resource_type,resourceId):
		print("--------------------------------------------------------------------------------------------")
		print("|                     Starting to upload proxy on hybrid                                   |")
		print("--------------------------------------------------------------------------------------------")

		#resourceId="apiProxyId"
		url = "https://apigee.googleapis.com/v1/organizations/"+org+"/"+resource_type+"?action=import&name="+filename+"&"+resourceId+" ="+filename
		payload={}
		files=[('file',(filename+'_new.zip',open(path+"\\"+filename+"\\"+filename+"_new.zip",'rb'),'application/zip'))]
		headers = {'Authorization': 'Bearer '+token}
		response = requests.request("POST", url, headers=headers, data=payload, files=files)
		status_code = response.status_code
		successful_upload = []
		if status_code ==200:
			successful_upload.append(filename)
			print("--------------------------------------------------------------------------------------------")
			print("|                      PROXY WAS UPLOADED SUCCESSFULLY                                     |")
			print("--------------------------------------------------------------------------------------------")
			print(successful_upload)
			#print(response.text)
		if status_code == 401:
			print("--------------------------------------------------------------------------------------------")
			print("|                       !!! ERROR UNAUTHORIZED !!!                                         |")
			print("--------------------------------------------------------------------------------------------")

			print(response.text)
			#exit()
		if status_code == 400:
			print("--------------------------------------------------------------------------------------------")
			print("   					  !!! ERROR The Zip Bundle Contains Error !!!                         |")
			print("--------------------------------------------------------------------------------------------")

			print(response.text)
			#exit()


class Deploy:
	"""docstring for ClassName"""
	def __init__(self):
		super(Deploy, self).__init__()

	def deploy_to_hybrid(evn,filename,token,org,resource_type):
		#resource_counter=resource_counter+1
		#print("<===================== Total Deployed Counter ==========================>" +str(resource_counter))
		print("--------------------------------------------------------------------------------------------")
		print("|                     Starting to Deploy proxy on hybrid                                   |")
		print("--------------------------------------------------------------------------------------------")
		url = "https://apigee.googleapis.com/v1/organizations/"+org+"/environments/"+evn+"/"+resource_type+"/"+filename+"/revisions/1/deployments"
		payload={}
		headers = {'Content-Type': 'application/json','Authorization': 'Bearer '+token}
		response = requests.request("POST", url, headers=headers, data=payload)
		status_code = response.status_code
		successful_deploy = []
		if status_code ==200:
			successful_deploy.append(filename)
			print("--------------------------------------------------------------------------------------------")
			print("|                      PROXY WAS DEPLOYED SUCCESSFULLY                                     |")
			print("--------------------------------------------------------------------------------------------")
			print(successful_deploy)
			#print(response.text)
		if status_code == 401:
			print("--------------------------------------------------------------------------------------------")
			print("|                       !!! ERROR UNAUTHORIZED !!!                                         |")
			print("--------------------------------------------------------------------------------------------")

			print(response.text)
			#exit()
		if status_code == 400:
			print("--------------------------------------------------------------------------------------------")
			print("   					  !!! ERROR The Zip Bundle Contains Error !!!                         |")
			print("--------------------------------------------------------------------------------------------")

			print(response.text)
		



