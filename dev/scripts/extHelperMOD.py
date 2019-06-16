import os
import subprocess
import platform

def Check_dep(debug=False):
	'''
		Check for dependencies and project path.
		
		This method checks to see if the path for the project is included in sys.path.
		This will ensure that the python modules used in the project will 
		be respected by the Touch.
		                
		Notes
		---------------
		'self' does not need to be included in the Args section.
		
		Args
		---------------
		debug (bool):
		> a bool to allow for us to print out the content of sys.path
								
		Returns
		---------------
		None
	'''

	# our path for all non-standard python modules
	dep_path 		= '{}/dep/python/'.format(project.folder)

	# if our path is already present we can skip this step
	if dep_path in sys.path:
		pass

	# insert the python path into our sys.path
	else:
		sys.path.insert(0, dep_path)

	# print each path in sys.path if debug is true:
	if debug:

		for each in sys.path:
			print(each)
	else:
		pass

	pass

def Install_python_external():
	'''
		Check and install any external modules.
		
		This method will go through all the necessary steps to enesure
		that our external modules are loaded into our project specific
		location. This approach assumes that external libraries should be 
		housed with the project, rather than with the standalone python
		installation, or with the Touch Installation. This ensrues a more consistent, 
		reliable, and portable approach when working with non-standard python
		modules. 
		                
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

		# change file permissions for the file
		subprocess.call(['chmod', '755', mac_py_dep])

		# change file to be executable
		subprocess.call(['chmod', '+x', mac_py_dep])

		# check to see if there is anything in the python dep dir
		# for now we'll assume that if there are files here we
		# successfully installed our python dependencies
		if len(os.listdir(python_path)) == 0:
			print("Running Install Script")
			subprocess.Popen(["open", "-a", "Terminal.app", mac_py_dep])
		else:
			pass

	else:
		pass

	return

def win_dep(requirementsPath, targetPath):
	'''
		Format text for command line execution.
		
		This method returns a formatted script to be executed by windows to
		both upgrade pip, and install any modules listed in the requirements
		DAT.
		                
		Notes
		---------------
		'self' does not need to be included in the Args section.
		
		Args
		---------------
		requirementsPath (str):
		> a string path to the requirements txt doc

		targetPath (str):
		> a string path to the target installation directory

		Returns
		---------------
		formatted_win_txt (str):
		> the formatted text for a .cmd file for automated installation
	'''
	win_txt = ''':: Update dependencies

:: make sure pip is up to date
python -m pip install --user --upgrade pip

:: install requirements
pip install -r {reqs}/requirements.txt --target="{target}"'''

	formatted_win_txt = win_txt.format(reqs=requirementsPath, target=targetPath)
	
	return formatted_win_txt


def mac_dep(requirementsPath, targetPath):
	'''
		Format text for command line execution.
		
		This method returns a formatted script to be executed by macOS to
		both upgrade pip, and install any modules listed in the requirements
		DAT.
		                
		Notes
		---------------
		'self' does not need to be included in the Args section.
		
		Args
		---------------
		requirementsPath (str):
		> a string path to the requirements txt doc

		targetPath (str):
		> a string path to the target installation directory

		Returns
		---------------
		formatted_mac_txt (str):
		> the formatted text for a .sh file for automated installation
	'''
	mac_txt = '''
#!/bin/bash 

dep=$(dirname "$0")
pythonDir=/python

# change current direcotry to where the script is run from
dirname "$(readlink -f "$0")"

# fix up pip with python3
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py

# Update dependencies

# make sure pip is up to date
python3 -m pip install --user --upgrade pip

# install requirements
python3 -m pip install -r {reqs}/requirements.txt --target={target}'''
	formatted_mac_txt = mac_txt.format(reqs=requirementsPath, target=targetPath)
	return formatted_mac_txt