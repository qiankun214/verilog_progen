import os
import shutil
import argparse
from filelistgen import depend_detector

# comment
parser = argparse.ArgumentParser()
parser.add_argument("module", help="module name you want to nlint")
parser.add_argument("-s", "--simmode",help="simmode pre or post",default="pre")
parser.add_argument("-m", "--makefile",help="use makefile to nlint,default is true",action='store_false',default=True)
parser.add_argument("-p", "--pre",help="nlint order name in makefile module,default is make",default="make")
parser.add_argument("-i", "--info_root", help="root path of info",default="info")
args = parser.parse_args()

module = args.module
simmode = args.simmode
is_makefile = args.makefile
pre_make = args.pre
info_root = args.info_root

# build workspace
if os.path.exists("verdi_workspace"):
    print("WARNING:dir verdi_workspace exists,delete it")
    shutil.rmtree("verdi_workspace")
os.mkdir("verdi_workspace")

# generate filelist
if not os.path.exists(info_root):
    raise ValueError("FATAL:info root {} not exists".format(info_root))
info_path = os.path.join(info_root,"{}.json".format(module))
if not os.path.exists(info_path):
    raise ValueError("FATAL:module info path {} not exists".format(info_path))
dd = depend_detector(module,info_root=info_root)
filelist = dd.gen_filelist()
filelist = [dd.info['tb_path'],] + filelist
with open("verdi_workspace/sim_filelist.f",'w') as f:
    f.write("\n".join(filelist))

# check fsdb
fsdb_path = os.path.join("fsdb","{}_{}.fsdb".format(module,simmode))
if not os.path.exists("fsdb"):
    raise ValueError("FATAL:fsdb root not exists")
if not os.path.exists(fsdb_path):
    raise ValueError("FATL:cannot find {} in fsdb dir".format(fsdb_path))

# build order
order = ["verdi -sv -ssf {}".format(fsdb_path)]
order.append("-f verdi_workspace/sim_filelist.f")
order.append("-logdir verdi_workspace/verdiLog -guiConf verdi_workspace/novas.conf -rcFile verdi_workspace/novas.rc")
order.append("| tee verdi_workspace/verdi.log")
order = " ".join(order)

# run
if is_makefile:
    if os.path.exists("makefile"):
        print("WARNING:makefile already exists,rename it as makefile_old")
        if os.path.exists("makefile_old"):
            os.remove("makefile_old")
        os.rename("makefile","makefile_old")
    with open("makefile",'w') as f:
        f.write(r"export LD_LIBRARY_PATH := ${LD_LIBRARY_PATH}:/app/synopsys/verdi1403/share/PLI/VCS/LINUX64"+"\n")
        # f.write(r"export NOVAS_HOME := /app/synopsys/verdi1403"+"\n")
        f.write("verdi:\n")
        f.write("\t{}".format(order))
    shutil.copy("makefile","verdi_workspace/makefile")
    os.system("{} verdi".format(pre_make))
else:
    os.system(order)