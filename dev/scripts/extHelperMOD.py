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
 
	Dep_path 		= '{}/dep'.format(project.folder)
	phue_path 		= '{}/dep/python/phue.py'.format(project.folder)
	win_py_dep 		= '{}/dep/update-dep-python-windows.cmd'.format(project.folder)
	mac_py_dep 		= '{}/dep/update-dep-python-mac.sh'.format(project.folder)

 	# check to see if /dep is in the project folder
	if os.path.isdir(Dep_path):
		pass
	# create the direcotry if it's not there
	else:
		os.mkdir(Dep_path)

	# check to see if our requirements elements are in place
	has_win_py 		= os.path.isfile(win_py_dep)
	has_mac_py 		= os.path.isfile(mac_py_dep)

	win_py_txt 		= me.mod.extHelperMOD.win_dep()
	mac_py_txt 		= me.mod.extHelperMOD.mac_dep()

	if has_win_py and has_mac_py:
		pass
	else:
		win_file 	= open(win_py_dep, 'w')
		win_file.write(win_py_txt)
		win_file.close()

		mac_file 	= open(mac_py_dep, 'w')
		mac_file.write(mac_py_txt)
		mac_file.close()

	# identify platform
	osPlatform 		= platform.system()

	# on windows run the file in command line
	if osPlatform == "Windows":
		if os.path.isfile(phue_path):
			pass
		else:
			subprocess.Popen([win_py_dep])
	
	elif osPlatform == "Darwin":
		if os.path.isfile(phue_path):
			pass
		else:
			subprocess.Popen([mac_py_dep])
	else:
		pass

	return

def win_dep():
    win_txt = '''
:: Update dependencies

:: make sure pip is up to date
python -m pip install --upgrade pip

:: pull phue
pip install --target="%~dp0\python" phue'''

    return win_txt

def mac_dep():
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

# pull phue
python3 -m pip install --target=$dep$pythonDir phue
'''
    return mac_txt