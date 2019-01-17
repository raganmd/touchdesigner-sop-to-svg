import os
import subprocess
import platform

def Check_dep():
	'''
		This is a sample method.
		
		This sample method is intended to help illustrate what method docstrings should look like.
		                
		Notes
		---------------
		'self' does not need to be included in the Args section.
		
		Args
		---------------
		None
								
		Returns
		---------------
		None
	'''

	Dep_path 		= '{}/dep/python/'.format(project.folder)

	if Dep_path in sys.path:
		pass

	else:
		sys.path.insert(0, Dep_path)

	for each in sys.path:
		print(each)

	return

def Check_dep_path():
	'''
		This method checks for and creates a dep path.
		
		More here shortly.
		                
		Notes
		---------------
		'self' does not need to be included in the Args section.
		
		Args
		---------------
		None
								
		Returns
		---------------
		None
	'''
 
	dep_path 			= '{}/dep'.format(project.folder)
	python_path 		= '{}/dep/python'.format(project.folder)
	scripts_reqs_path 	= '{proj}/dep/{name}'.format(proj=project.folder, name=parent().par.Name)
	requirements 		= '{}/requirements.txt'.format(scripts_reqs_path)
	reqs_dat 			= op('reqs')
	phue_path 			= '{}/dep/python/phue.py'.format(project.folder)
	win_py_dep 			= '{}/update-dep-python-windows.cmd'.format(scripts_reqs_path)
	mac_py_dep 			= '{}/update-dep-python-mac.sh'.format(scripts_reqs_path)

 	# check to see if /dep is in the project folder
	if os.path.isdir(dep_path):
		pass
	# create the direcotry if it's not there
	else:
		os.mkdir(dep_path)

 	# check to see if /python is in the project folder
	if os.path.isdir(python_path):
		pass
	# create the direcotry if it's not there
	else:
		os.mkdir(python_path)

 	# check to see if there's a scripts and requirements folder
	if os.path.isdir(scripts_reqs_path):
		pass
	# create the direcotry if it's not there
	else:
		os.mkdir(scripts_reqs_path)

	# check to see if the requirements txt is in place
	if os.path.isfile(requirements):
		pass
	else:
		reqs_file 	= open(requirements, 'w')
		reqs_file.write(reqs_dat.text)
		reqs_file.close()

	# check to see if our auto-generaetd scripts are in place
	has_win_py 		= os.path.isfile(win_py_dep)
	has_mac_py 		= os.path.isfile(mac_py_dep)

	win_py_txt 		= me.mod.extHelperMOD.win_dep(scripts_reqs_path, python_path)
	mac_py_txt 		= me.mod.extHelperMOD.mac_dep(scripts_reqs_path, python_path)

	# identify platform
	osPlatform 		= platform.system()

	# on windows
	if osPlatform == "Windows":
		# create the script to handle grabbing our dependencies
		req_file 	= open(win_py_dep, 'w')
		req_file.write(win_py_txt)
		req_file.close()

		# check to see if there is anything in the python dep dir
		# for now we'll assume that if there are files here we
		# successfully installed our python dependencies
		if len(os.listdir(python_path)) == 0:
			subprocess.Popen([win_py_dep])
		else:
			pass				
	# on mac
	elif osPlatform == "Darwin":
		# create the script to handle grabbing our dependencies
		mac_file 	= open(mac_py_dep, 'w')
		mac_file.write(mac_py_txt)
		mac_file.close()

		# check to see if there is anything in the python dep dir
		# for now we'll assume that if there are files here we
		# successfully installed our python dependencies
		if len(os.listdir(python_path)) == 0:
			subprocess.Popen([mac_py_dep])
		else:
			pass

	else:
		pass

	return

def win_dep(requirementsPath, targetPath):
	win_txt = ''':: Update dependencies

:: make sure pip is up to date
python -m pip install --upgrade pip

:: install requirements
pip install -r {reqs}/requirements.txt --target="{target}"'''

	formatted_win_txt = win_txt.format(reqs=requirementsPath, target=targetPath)
	
	return formatted_win_txt

def mac_dep(requirementsPath, targetPath):
	mac_txt = '''
#!/bin/bash 

dep=$(dirname "$0")
pythonDir=/python

# change current direcotry to where the script is run from
dirname "$(readlink -f "$0")"

# permission to run the file
sudo chmod 755 udpate-dep-python-mac.sh

# fix up pip with python3
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py

# Update dependencies

# make sure pip is up to date
python3 -m pip install --upgrade pip

# install requirements
python3 -m pip install -r {reqs}/requirements.txt --target={target}'''
	formatted_mac_txt = mac_txt.format(reqs=requirementsPath, target=targetPath)
	return formatted_mac_txt