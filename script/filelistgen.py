import json
import os
import re
import argparse

class depend_detector(object):

    def __init__(self,info_path,info_root="./info/"):
        self.info_path = os.path.join(info_root,"{}.json".format(info_path))
        self.info_root = info_root
        self.info = self._read_json(self.info_path)
        self.depent_list = []
        self.sv_depend_list = []

    def _read_json(self,path):
        with open(path,'r') as f:
            return json.load(f)

    def _ds_depend_find(self,info):
        if info['ds_path'] in self.depent_list:
            return
        self.depent_list.append(info['ds_path'])
        if info.get("link") is None:
            return
        for i in info['link']['submodule']:
            data = info['link']['submodule'][i]
            submodule_name = data['module']
            submodule_path = os.path.join(self.info_root,"{}.json".format(submodule_name))
            print("INFO:find module {} depend {}".format(info['name'],submodule_name))
            self._ds_depend_find(self._read_json(submodule_path))

    def _sv_depend_find(self,path):
        if path in self.sv_depend_list:
            return
        self.sv_depend_list.append(path)
        with open(path,'r') as f:
            content = f.read()
        if re.search(r'`include\s*"(\w+)"',content) is not None:
            depent = re.findall(r'`include\s*"\w+"',content)
            for p in depent:
                print("INFO:find testbench {} depend {}".format(path,p))
                self._sv_depend_find(p)
        
    def _write(self,path,need_sv=True):
        final_list = self.depent_list.copy()
        if need_sv is True:
            final_list = self.sv_depend_list + final_list
        with open(path,'w') as f:
            f.write("\n".join(final_list))

    def __call__(self,filelist_path,need_sv=True):
        self._ds_depend_find(self.info)
        if need_sv:
            self._sv_depend_find(self.info['tb_path'])
        self._write(filelist_path,need_sv)
        print("INFO:filelist of {} generate successful".format(self.info['name']))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verilog", help="module name to generate filelist")
    parser.add_argument("-o", "--output", help="filelist path",default="./simfile/simfile_rtl.f")
    parser.add_argument("-i", "--info_root", help="info root",default="./info")
    parser.add_argument("-t", "--testbench",help="need testbench in filelist",action='store_true')
    args = parser.parse_args()
    generator = depend_detector(args.verilog,args.info_root)
    generator(args.output,args.testbench)
