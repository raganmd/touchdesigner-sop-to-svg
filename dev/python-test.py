import subprocess
import sys

pythonEvnVar = "python"
reqs = "E:/github/ragan-git/touchdesigner/_tools/touchdesigner-sop-to-svg/dev/dep/sop-to-svg/requirements.txt"
install_loc = "E:/github/ragan-git/touchdesigner/_tools/touchdesigner-sop-to-svg/dev/dep/python"

def pip_install(pythonEvnVar, reqs, install_loc):
    run_str = '{pythonEnv} -m pip install -r {reqs} --target={install_loc}'.format(pythonEnv=pythonEvnVar, reqs=reqs, install_loc=install_loc)
    subprocess.run(run_str)
    # subprocess_args = [pythonEvnVar, '-m', 'pip', 'install', '-r', "{}".format(reqs), '--target', "{}".format(install_loc)]
	# print(subprocess_args)
	# subprocess.call(subprocess_args)

pip_install(pythonEvnVar, reqs, install_loc)


