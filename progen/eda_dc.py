from dc_tcl_library import generate_dc_grouppath, generate_dc_optimizer, generate_dc_report
from lib_decoder import compiler_lib_info
from utils import build_workspace,write_makefile
from submit import submit_module_gen
from module_info import module_info
from dc_tcl_library import generate_dc_sdc,generate_dc_readrtl,generate_dc_writeresult
import argparse,os

parser = argparse.ArgumentParser()
parser.add_argument("-n", "--name",help="module name you want to syn",default="")
parser.add_argument("-m", "--makefile",help="use makefile to nlint,default is true",action='store_false',default=True)
parser.add_argument("-p", "--pre",help="nlint order name in makefile module,default is make",default="make")
parser.add_argument("-i", "--info_root", help="root path of info",default="info")
parser.add_argument("-r", "--run",help="run dc script,default is false",action='store_true',default=False)
parser.add_argument("-s", "--script",help="not rewrite script,default is true(no rewrite)",action='store_false',default=True)
parser.add_argument("-c", "--cycle",help="clock cycle",type=float,default=-1)
parser.add_argument("lib_path",help="path of lib json",default="lib.json")
parser.add_argument("--input",help="input delay factor",type=float,default=0.6)
parser.add_argument("--output",help="output delay factor",type=float,default=0.6)
parser.add_argument("--uncertainty",help="output delay factor",type=float,default=0.3)

args = parser.parse_args()

module = args.name
is_makefile = args.makefile
pre_make = args.pre
info_root = args.info_root
is_run = args.run
is_script = args.script
cycle = args.cycle
input_factor = args.input
output_factor = args.output
uncertainty = args.uncertainty
lib_path = args.lib_path
if cycle <= 0:
    raise ValueError("FATAL:cycle must be specified")
if len(module) == 0:
    raise ValueError("FATAL:module must be specified")

input_file_root = os.path.join("dc_workspace","input")
output_file_root = os.path.join("dc_workspace","output")
report_file_root = os.path.join("dc_workspace","report")
script_file_root = os.path.join("dc_workspace","script")
milkway_file_root = os.path.join("dc_workspace","milkway")
json_path = os.path.join(info_root,"{}.json".format(module))

# load old script
script_path = os.path.join(script_file_root,"dc.tcl")
sdc_path = os.path.join(script_file_root,"sdc.tcl")
old_script,old_sdc = None,None
if is_script:

    if os.path.exists(script_path):
        with open(script_path,'r') as f:
            old_script = f.read()
    else:
        print("WARNING:{} not exists,rewrite it".format(script_path))

    if os.path.exists(sdc_path):
        with open(sdc_path,'r') as f:
            old_sdc = f.read()
    else:
        print("WARNING:{} not exists,rewrite it".format(sdc_path))

# build workspace

build_workspace("dc_workspace")
os.mkdir(input_file_root)
os.mkdir(output_file_root)
os.mkdir(report_file_root)
os.mkdir(script_file_root)
os.mkdir(milkway_file_root)

# generate input verilog and filelist
filelist,content = submit_module_gen(module,info_root)
with open(os.path.join(input_file_root,"{}.v".format(module)),'w') as f:
    f.write(content)
with open(os.path.join(input_file_root,"{}.f".format(module)),'w') as f:
    f.write("\n".join(filelist))

# generate sdc script
info = module_info(json_path)
clock = info.get_clklist()
if len(clock) != 1:
    print("ERROR:mult clock detect,this script only can handle single clock")
if old_sdc is None or not is_script:
    old_sdc = generate_dc_sdc(cycle,clock[0],uncertainty,input_factor,output_factor)
with open(sdc_path,'w') as f:
    f.write(old_sdc)
print("INFO:write sdc to {}".format(sdc_path))

# generate dc script
if not is_script or old_script is None:
    lib = compiler_lib_info(lib_path)
    lib.load()
    print(lib.sc_lib.fast_db)
    content = [lib.generate_lib_def(),lib.generate_mw_build(os.path.join(milkway_file_root,module))]
    content.append(generate_dc_readrtl(module,"dc_workspace",os.path.join(input_file_root,"{}.v".format(module))))
    content.append(generate_dc_grouppath())
    content.append("source dc_workspace/script/sdc.tcl")
    content.append(generate_dc_optimizer(module,"dc_workspace"))
    content.append(generate_dc_writeresult(module,output_file_root))
    content.append(generate_dc_report(module,report_file_root))
    content.append("exit")

    old_script = "\n\n".join(content)
with open(os.path.join(script_file_root,"dc.tcl"),'w') as f:
    f.write(old_script)

# generate makefile
order = "dc_shell-xg-t -topo -no_gui -f ./dc_workspace/script/dc.tcl | tee ./dc_workspace/dc.log"
if is_makefile:
    write_makefile("dc",order,"dc_workspace")

# run
if is_run:
    if is_makefile:
        os.system("{} dc".format(pre_make))
    else:
        os.system(order)