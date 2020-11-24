import json
import os

class module_info(object):

    def __init__(self,json_path):
        super(module_info,self).__init__()
        if isinstance(json_path,str) and os.path.exists(json_path):
            with open(json_path,'r') as f:
                info = json.load(f)
        elif isinstance(json_path,dict):
            info = json_path
        else:
            raise ValueError("FATAL:{} is not a path or dict".format(json_path))
        self._pre_handle(info)

    def _pre_handle(self,info):
        self.parameter = info["parameter"]
        self.link = info["link"]
        self.name = info["name"]
        self.ds_path = info["ds_path"]
        self.tb_path = info["tb_path"]
        
        self.port = info["port"]
        self.input_port,self.output_port = [],[]
        for port_name in self.port:
            if "in" in self.port[port_name][0]:
                self.input_port.append(port_name)
            else:
                self.output_port.append(port_name)

    def moduledef_gen(self):
        pass

    def instance_gen(self):
        pass

    def testbench_gen(self):
        pass

    def design_gen(self):
        pass

