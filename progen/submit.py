import argparse,os
from filelistgen import depend_detector

def submit_module_gen(module_name,root):
    d = depend_detector(module_name,root)
    d._ds_depend_find(d.info)
    filelist = d.depent_list.copy()
    print("INFO:submit file list:\n{}".format("\n".join(filelist)))
    content_list = []
    for path in filelist:
        content_list.append("// {}".format(path))
        with open(path,'r') as f:
            content_list.append(f.read())
        content_list.append("")
    return "\n".join(content_list)

def submit_module_write(module_name,content,save_root="."):
    target_path = os.path.join(save_root,"SUBMIT_{}.v".format(module_name))
    if os.path.exists(target_path):
        print("WARING:{} already exists,rename it as {}.old".format(target_path,target_path))
        if os.path.exists("{}.old".format(target_path)):
            print("INFO:delete file {}.old".format(target_path))
            os.remove("{}.old".format(target_path))
        os.rename(target_path,"{}.old".format(target_path))
        print("INFO:rename successful")
    with open(target_path,'w') as f:
        f.write(content)
    print("INFO:submit file write finish")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("verilog", help="module name to submit")
    parser.add_argument("-o", "--output", help="submit file root",default="./")
    parser.add_argument("-i", "--info_root", help="info root",default="./info")
    args = parser.parse_args()

    result = submit_module_gen(args.verilog,args.info_root)
    submit_module_write(args.verilog,result,args.output)