import argparse,os
from filelistgen import depend_detector
from utils import build_workspace,write_makefile

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
    return filelist,"\n".join(content_list)

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
    parser.add_argument("-i", "--info_root", help="info root",default="./info")
    parser.add_argument("-m", "--makefile",help="use makefile to nlint,default is true",action='store_false',default=True)
    parser.add_argument("-p", "--pre",help="nlint order name in makefile module,default is make",default="make")
    args = parser.parse_args()

    build_workspace("submit_workspace")
    _,result = submit_module_gen(args.verilog,args.info_root)
    submit_module_write(args.verilog,result,"submit_workspace")

    # nlint check
    nlint_order = "nLint -95 -2001 -beauty -rs ./nLint/my_nLint.rs -logdir submit_workspace/nLintLog -rdb submit_workspace/nLintDB -out submit_workspace/{name}_nlint.log -top {name} submit_workspace/SUBMIT_{name}.v".format(name=args.verilog)
    if args.makefile:
        write_makefile("submit",nlint_order,"submit_workspace")
        os.system("{} submit".format(args.pre))
    else:
        os.system(nlint_order)
        
