import shutil
import sys
import os
import zipfile as zp


class Unzip:
	"""This will extract the contents of a zipped files"""
	def __init__(self):
		super(Unzip, self).__init__()

	def unzip_file(filename,path):
		from zipfile import ZipFile
		try:
			ZipFile(filename+".zip").extractall(path)
			print("<=========================== PROXY PATH =======================================>"+path)
		except IOError:
			#pass
			print('Specified Zip File not found ')	

class Zip:
	"""docstring for Zip's the edited file"""
	def __init__(self):
		super(Zip, self).__init__()

	def create_newzip_after_changes(filename,path):
		#print(os.getcwd())
		os.chdir(path+"\\"+filename)
		#print("<============================== CURRENT DIRECTORY ==================================>"+os.getcwd())
		print("--------------------------------------------------------------------------------------------")
		print("|                             Creating a zip bundle                                        |")
		print("--------------------------------------------------------------------------------------------")
		shutil.make_archive(filename, 'zip', path+"\\"+filename)
		zin = zp.ZipFile (filename+'.zip', 'r')
		zout = zp.ZipFile (filename+'_new.zip', 'w')
		for item in zin.infolist():
			buffer = zin.read(item.filename)
			if (item.filename[-4:] != '.zip'):
				zout.writestr(item, buffer)
		zout.close()
		zin.close()
		print("--------------------------------------------------------------------------------------------")
		print("|                               Zip Bundle Created                                         |")
		print("--------------------------------------------------------------------------------------------")
		os.chdir(path)
		
