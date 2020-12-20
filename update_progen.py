import os
import argparse
import shutil

# commetn
parser = argparse.ArgumentParser()
parser.add_argument("path",type=str,help="target path")
args = parser.parse_args()
path = args.path

# check target path
if not os.path.exists(path):
    raise ValueError("FATAL:project {} not exists".format(path))

# generate path
this_root = os.path.split(os.path.abspath(__file__))[0]
progen_path = os.path.join(this_root,"progen")
target_path = os.path.join(path,"progen")

# remove old progen
if os.path.exists(target_path):
    shutil.rmtree(target_path)
    print("INFO:delete old progen successful")
else:
    print("WARNING:progen not find")

# copy new progen
shutil.copytree(progen_path,target_path)
print("INFO:progen update successful")