from data_structure import module_info,vfile_analysis
import os
import argparse

def filelist_generate(root,result_path,module_path=None):
    file_list = [os.path.join(root,x) for x in os.listdir(root) if x[-2:] == ".v"]
    if module_path is not None:
        file_list.append(module_path)
    module_dict = {}
    for path in file_list:
        minfo = vfile_analysis(path)
        for x in minfo:
            module_dict[x.name] = x
    root_node = vfile_analysis(module_path)[0]
    # module = root_node.name
    # if module_dict.get(module) is None:
        # raise ValueError("FATAL:no module {} in {}".format(module,root))
    # root_node = module_dict[module]
    path_list = []
    print(root_node.submodule_list)
    def get_path(node):
        # print("SSS",node)
        if node.path not in path_list:
            path_list.append(node.path)
        for i in node.submodule_list:
            # print(i)
            get_path(module_dict[i])
    get_path(root_node)
    with open(result_path,'w') as f:
        f.write("\n".join(path_list))
    return path_list

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help="top module file path")
    parser.add_argument("-r", "--root", help="root path of rtl file",default="./rtl")
    parser.add_argument("-o", "--output", help="output filelist path",default="./simfile/rtl.list")
    args = parser.parse_args()
    input_path = args.file
    output_path = args.output
    root_path = args.root
    a = filelist_generate(
        root=root_path,
        result_path=output_path,module_path=input_path)
    print(a)