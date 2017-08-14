import subprocess
from os import path
from sys import exit
import getpass
keyword = raw_input("[>] Enter a Keyword To Search: ")
base_directory="/Users/" + getpass.getuser() + "/.atom/packages/extraction-debugger/ExtractorsRepo/"
if (not path.exists(base_directory)):
    print "[!] Error - Path does not exists. did you typed your username correctly?"
    print "[!] Erroneous Path : "+base_directory
    exit(1)
command = "cd ~/.atom/packages/extraction-debugger/ExtractorsRepo && git pull && git ls-files"
files_path = subprocess.check_output(command, shell=True).split("\n")
for filename in files_path:
    if(path.isfile(base_directory+filename)):
        with open(base_directory+filename, 'r') as infile:
            if (keyword in ''.join(infile.readlines())):
                print "[#] Found one : "+filename
