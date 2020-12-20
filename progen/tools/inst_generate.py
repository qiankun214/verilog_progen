import argparse
from data_structure import vfile_analysis,module_info
import pyperclip

def generate_inst(input_path,module_name):
    analysiser = vfile_analysis(input_path)
    if module_name == "default":
        module_info = analysiser[0]
    else:
        for m in analysiser:
            if m.name == module_name:
                module_info = m
                break
        raise ValueError("ERROR:cannot find module {} in {}".format(module_name,input_path) )
    inst_str = module_info.inst("inst_{}".format(module_info.name))
    print(inst_str)
    pyperclip.copy(inst_str)
    print("Info:inst push in your clipboard")
    return inst_str

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help="input verilog file")
    parser.add_argument("-m", "--module", help="module name",default="default")
    args = parser.parse_args()
    input_path = args.file
    module_name = args.module
    generate_inst(input_path,module_name)