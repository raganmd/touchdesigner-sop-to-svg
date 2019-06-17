import wget
import json
import os

# vars for execution
release_dir = "releaseVersions"
json_file_ext = "releaseFiles.json"

# a function to check for and create our release_dir if necessary
def check_for_dir():
    if os.path.isdir(release_dir):
        pass
    else:
        print("Creating releaseVersions directory")
        os.mkdir(release_dir)
    pass

# a function to delete old versions
def delete_old_files(del_dir):
    # loop through all files in directory and delete them
    for each_file in os.listdir(del_dir):
        target_file = '{}\{}'.format(del_dir, each_file)
        os.remove(target_file)
        print('deleting {}'.format(target_file))
    pass

# a function to download new files as described in external file
def download_files(json_file_with_externals):
    # open extenral file and create python dictionary out of json
    allRemotes = open(json_file_with_externals, "r")
    workingDict = json.load(allRemotes)
    allRemotes.close()

    # loop through all entries and download them to the directory specified
    for each_remote in workingDict['targets']:
        save_name = each_remote['name']
        target_url = each_remote['url'] 

        target_path = "{dir}\\{file}.tox".format(dir=release_dir, file=save_name)
        wget.download(target_url, target_path)    

        print("\ndownloading {save_url} \nsaving to {target_path} \n".format(target_path=target_path, save_url=target_url))
    pass

# check for directory
print("Checking for releaseVersions directory")
check_for_dir()

# delete old files
print("Deleting Old Files")
delete_old_files(release_dir)

print('- ' * 5)
print('\n')

# download latest release versions - these are all from master branches
print("Downloading New Files")
download_files(json_file_ext)