import re
import os
import json

class md2json(object):
    
    def __init__(self,md_path,js_root):
        super(md2json,self).__init__()
        self.md_path = md_path
        self.js_path = self.js_path_gen(js_root)
        self.data_paramter = None
        self.data_port = None
        self.data_link = None
        self.js_data = {}

    def js_path_gen(self,js_root):
        module_name = os.path.splitext((os.path.split(self.md_path)[1]))[0]
        return os.path.join(js_root,"{}.json".format(module_name))

    def read(self):
        module_name = os.path.splitext((os.path.split(self.md_path)[1]))[0]
        self.js_data['name'] = module_name
        with open(self.md_path,'r') as f:
            content = f.read()
        data = re.split(r"\n\s*#\s*\b",content)
        # print(data)
        if len(data) == 2:
            self.data_paramter,self.data_port = data
            self.data_link = None
        elif len(data) == 3:
            self.data_paramter,self.data_port,self.data_link = data
            if "=" not in self.data_link:
                self.data_link = None
        else:
            # print(data)
            raise ValueError("error")
    def write(self):
        with open(self.js_path,'w') as f:
            json.dump(self.js_data,f,indent=4)

    def _paramter_table(self):
        tmp,self.js_data['parameter'] = [],{}
        # print(self.data_paramter)
        for line in self.data_paramter.split("\n"):
            if "|" in line:
                this_data = [x.strip() for x in line.split("|")[1:-1]]
                # print(this_data)
                if len(this_data[0]) == this_data[0].count("-"):
                    tmp = tmp[:-1]
                    continue
                tmp.append(this_data)
        for line in tmp:
            self.js_data['parameter'][line[0]] = [line[2],line[1]]
        # print(self.js_data['parameter'])
            
    def _port_table(self):
        tmp,self.js_data['port'] = [],{}
        # print(self.data_paramter)
        for line in self.data_port.split("\n"):
            if "|" in line:
                this_data = [x.strip() for x in line.split("|")[1:-1]]
                # print(this_data)
                if len(this_data[0]) == this_data[0].count("-"):
                    tmp = tmp[:-1]
                    continue
                tmp.append(this_data)
        for line in tmp:
            self.js_data['port'][line[0]] = line[1:]

    def _link_handle(self):
        pass

    def __call__(self):
        self.read()
        self._paramter_table()
        self._port_table()
        self._link_handle()
        # print(self.js_data)
        self.write()
        print("INFO:module '{}' from markdown to json finish".format(self.js_data['name']))

if __name__ == "__main__":
    test = md2json("../inputs/test.md",'../doc/')
    test()
