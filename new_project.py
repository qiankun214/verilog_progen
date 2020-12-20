import os
import argparse
from os import path


parser = argparse.ArgumentParser()
parser.add_argument("root", type=str,help="root of design")
parser.add_argument("-n","--name", type=str,help="name of design")
args = parser.parse_args()
root = args.root
name = args.name

# mkdir root dir
design_path = os.path.join(root,name)
if not os.path.exists(root):
    raise ValueError("FATAL:root {} not exists".format(root))
if os.path.exists(design_path):
    raise ValueError("FATAL:design {} already exists".format(design_path))
os.mkdir(design_path)

# mkdir useful dir
useful_dir = ["module_doc","rtl","testbench","info","simfile","log","syn","sdc","script","fsdb"]
for dir_name in useful_dir:
    dir_path = os.path.join(design_path,dir_name)
    os.mkdir(dir_path)

# copy dir 
copy_dir = ["progen","doc","example"]
this_root = os.path.split(os.path.abspath(__file__))[0]
for dir_name in copy_dir:
    dir_path = os.path.join(this_root,dir_name)
    os.system("cp -r {} {}".format(dir_path,design_path))

print("INFO:design generator successful")