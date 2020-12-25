import os
import shutil
import argparse
from filelistgen import depend_detector

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
if os.path.exists("vcs_workspace"):
    print("WARNING:dir vcs_workspace exists,delete it")
    shutil.rmtree("vcs_workspace")
os.mkdir("vcs_workspace")
if not os.path.exists("fsdb"):
    os.mkdir("fsdb")

# depend_detector
if not os.path.exists(info_root):
    raise ValueError("FATAL:info root {} not exists".format(info_root))
info_path = os.path.join(info_root,"{}.json".format(module))
if not os.path.exists(info_path):
    raise ValueError("FATAL:module info path {} not exists".format(info_path))
dd = depend_detector(module,info_root=info_root)
filelist = dd.gen_filelist()
filelist = [dd.info['tb_path'],] + filelist
with open("vcs_workspace/sim_filelist.f",'w') as f:
    f.write("\n".join(filelist))

# build order
order = ["vcs -debug_pp -R -full64 +plusarg_save +v2k -sverilog +evalorder +no_notifier +vc -R"]
order.append("+define+DUMP +DUMP +FSDB=fsdb/{}_{}.fsdb".format(module,simmode))
order.append(r"-P $(VERDI_HOME)/share/PLI/VCS/LINUX64/novas.tab $(VERDI_HOME)/share/PLI/VCS/LINUX64/pli.a")

order.append("+notimingcheck -o vcs_workspace/simv -ova_report vcs_workspace/ova.log")
order.append("-l vcs_workspace/runtime.log")
order.append("+csdf+precomp+dir+vcs_workspace")
order.append("-f ./vcs_workspace/sim_filelist.f")
order.append("| tee vcs_workspace/vcs_{}.log".format(module))

order = " ".join(order)
print(order)
# -ntb_sfname <filename>
#    Specifies the filename of the testbench shell.

# -ntb_sname <module_name>
#    Specifies the name and directory where VCS writes the testbench shell 
#    module.

# -o name

# -a <filename>
#    Specifies appending all messages from simulation to the bottom of
#    the text in the specified file as well as displaying these messages
#    to the standard output.

#    report[=<filename>]
#       Generates a SystemVerilog assertion report file in addition to
#       displaying results on your screen. By default the file's name and
#       location is ./simv.vdb/report/ova.report, but you can change this
#       by entering the filename pathname argument.

# -grw <filename>
#    Sets the name of the $gr_waves output file to the specified file.
#    The default filename is grw.dump. 

# -ova_cov_name <filename>
#    Specifies the file name or the full path name of the functional coverage
#    report file. This option overrides the default report name and location.
#    If only a file name is given, the default location is used resulting in 
#    ./simv.vdb/fcov/<filename>.db.

# -ova_report [<filename>]
#    Specifies writing an OpenVera Assertions report file. The default file 
#    name and location is simv.vdb/report/ova.report but you can specify 
#    a different name and location as an argument to this option.

# +ntb_cache_dir=<path_name_to_directory>
#    Specifies the directory location of the cache that VCS maintains as an 
#    internal disk cache for randomization.

# -vpd_file <filename>
#    At runtime, defines an alternative name of the VPD file that VCS
#    writes instead of the default name vcdplus.vpd.

if is_makefile:
    if os.path.exists("makefile"):
        print("WARNING:makefile already exists,rename it as makefile_old")
        if os.path.exists("makefile_old"):
            os.remove("makefile_old")
        os.rename("makefile","makefile_old")
    with open("makefile",'w') as f:
        f.write(r"export LD_LIBRARY_PATH := ${LD_LIBRARY_PATH}:/app/synopsys/verdi1403/share/PLI/VCS/LINUX64"+"\n")
        f.write(r"export NOVAS_HOME := /app/synopsys/verdi1403"+"\n")
        f.write("vcs:\n")
        f.write("\t{}".format(order))
    shutil.copy("makefile","vcs_workspace/makefile")
    os.system("{} vcs".format(pre_make))
else:
    os.system(order)

if os.path.exists("novas_dump.log"):
    shutil.move("novas_dump.log","vcs_workspace/novas_dump.log")
if os.path.exists("ucli.key"):
    shutil.move("ucli.key","vcs_workspace/ucli.key")