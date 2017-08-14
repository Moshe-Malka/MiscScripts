# Moshe Malka
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
try:
    command = "cd ~/.atom/packages/extraction-debugger/ExtractorsRepo && git pull && git ls-files"
    files_paths = subprocess.check_output(command, shell=True).split("\n")
except subprocess.CalledProcessError as err:
    print "[!] CalledProcessError ({0}) : {1}".format(err.returncode ,err.output)
    print "Please check if Git is installed on your system."
    exit(1)
flag=False
print "[#] DSL's to Inspect : "+ str(len(files_paths))
try:
    for filename in files_paths:
        if(path.isfile(base_directory+filename)):
            with open(base_directory+filename, 'r') as infile:
                if (keyword in ''.join(infile.readlines())):
                    flag=True
                    print "     [#] Found keyword in : "+filename
except OSError as err:
    print "[!] OSError ({0}) : {1}".format(err.errno ,err.message)
    exit(1)
if(not flag):
    print "[#] Could Not Find Keyword in Repository."
