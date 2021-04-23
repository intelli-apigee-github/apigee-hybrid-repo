import sys
import os
from os import path
import shutil
import zipfile as zp
import re
#from pyutil import filereplace
import pyutil
import json
import requests
import upload_n_deploy
import zip_n_unzip
import creating_kvm
from create_data_collector import Dc_store

class Edit_Shared_Flow:
	"""docstring for Edit_Shared_Flow"""
	def __init__(self):
		super(Edit_Shared_Flow, self).__init__()
	def edit_shared_flow(environment,current_path,name_sf,bearer_token,org):
		shareflows_folder_path=current_path+"\\sharedflows"
		resource_type="sharedflows"
		resource_id = "sharedflowId"
		zip_n_unzip.Unzip.unzip_file(name_sf,shareflows_folder_path+"\\"+name_sf)
		zip_n_unzip.Zip.create_newzip_after_changes(name_sf,shareflows_folder_path)
		upload_zip=upload_n_deploy
		upload_n_deploy.Upload.upload_to_hybrid(shareflows_folder_path,name_sf,bearer_token,org,resource_type,resource_id)
		upload_n_deploy.Deploy.deploy_to_hybrid(environment[0],name_sf,bearer_token,org,resource_type)		

