import json
import requests



class Upload:
	"""This class uploads the zip to hybrid"""
	def __init__(self):
		super(Upload, self).__init__()
		
	
	def upload_to_hybrid(path,filename,token,resource_type,resourceId):
		print("Starting to upload proxy in hybrid")
		#resourceId="apiProxyId"
		url = "https://apigee.googleapis.com/v1/organizations/apigee-hybrid-demo-305106/"+resource_type+"?action=import&name="+filename+"&"+resourceId+" ="+filename
		payload={}
		files=[('file',(filename+'_new.zip',open(path+"\\"+filename+"\\"+filename+"_new.zip",'rb'),'application/zip'))]
		headers = {'Authorization': 'Bearer '+token}
		response = requests.request("POST", url, headers=headers, data=payload, files=files)
		print(response.text)


class Deploy:
	"""docstring for ClassName"""
	def __init__(self):
		super(Deploy, self).__init__()

	def deploy_to_hybrid(evn,filename,token,resource_type):
		print("Starting to Deploy proxies on hybrid ")
		url = "https://apigee.googleapis.com/v1/organizations/apigee-hybrid-demo-305106/environments/"+evn+"/"+resource_type+"/"+filename+"/revisions/1/deployments"
		payload={}
		headers = {'Content-Type': 'application/json','Authorization': 'Bearer '+token}
		response = requests.request("POST", url, headers=headers, data=payload)
		print(response.text)
		



