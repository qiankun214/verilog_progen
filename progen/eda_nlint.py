import os
from os.path import split, splitext
import shutil
import argparse
from sys import path
from filelistgen import depend_detector

parser = argparse.ArgumentParser()
parser.add_argument("module", help="module name you want to nlint")
parser.add_argument("-a", "--macro",help="submodule of this module handle as macro cell",action='store_true',default=False)
parser.add_argument("-m", "--makefile",help="use makefile to nlint,default is true",action='store_false',default=True)
parser.add_argument("-p", "--pre",help="nlint order name in makefile module,default is make",default="make")
parser.add_argument("-i", "--info_root", help="root path of info",default="info")
args = parser.parse_args()

module = args.module
is_macro = args.macro
is_makefile = args.makefile
pre_make = args.pre
info_root = args.info_root

# build workspace
if os.path.exists("nlint_workspace"):
    print("WARNING:dir nlint_workspace exists,delete it")
    shutil.rmtree("nlint_workspace")
os.mkdir("nlint_workspace")

# depend_detector
if not os.path.exists(info_root):
    raise ValueError("FATAL:info root {} not exists".format(info_root))
info_path = os.path.join(info_root,"{}.json".format(module))
if not os.path.exists(info_path):
    raise ValueError("FATAL:module info path {} not exists".format(info_path))
dd = depend_detector(module,info_root=info_root)
filelist = dd.gen_filelist()

# build order
order = ["nLint -95 -2001 -beauty -rs ./nLint/my_nLint.rs -logdir nlint_workspace/nLintLog -rdb nlint_workspace/nLintDB"]
out_file = os.path.join("nlint_workspace","nlint_{}.log".format(module))
order.append("-out {}".format(out_file))
order.append("-top {}".format(module))
# print(order)
# print(filelist)
# -bf <file_name> : specify a file with a source file name list in which all modules in the file are treated as macro cells.
#    -top <top_module> : specify a top module when importing the design.
if is_macro:
    # macro_list = [os.path.splitext(os.path.split(x)[-1])[0] for x in filelist[1:]]
    macro_list = filelist[1:]
    # filelist = [filelist[0],]
    with open("./nlint_workspace/macro.f",'w') as f:
        f.write("\n".join(macro_list))
    order.append("-bf nlint_workspace/macro.f")
    # order.append("-bb")
    # order += ["{}".format(x) for x in macro_list]
order.append(" ".join(filelist))

# write markdown
order = " ".join(order)
# print(order)
if is_makefile:
    if os.path.exists("makefile"):
        print("WARNING:makefile already exists,rename it as makefile_old")
        if os.path.exists("makefile_old"):
            os.remove("makefile_old")
        os.rename("makefile","makefile_old")
    with open("makefile",'w') as f:
        f.write("nlint:\n")
        f.write("\t{}".format(order))
    shutil.copy("makefile","nlint_workspace/makefile")
    os.system("{} nlint".format(pre_make))
else:
    os.system(order)

