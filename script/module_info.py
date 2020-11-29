import json
import os

class module_info(object):

    def __init__(self,json_path):
        super(module_info,self).__init__()
        if isinstance(json_path,str) and os.path.exists(json_path):
            with open(json_path,'r',encoding='utf-8') as f:
                info = json.load(f)
        elif isinstance(json_path,dict):
            info = json_path
        else:
            raise ValueError("FATAL:{} is not a path or dict".format(json_path))
        self._pre_handle(info)

    def _pre_handle(self,info):
        self.parameter = info["parameter"]
        if info.get("link") is not None:
            self.link = info["link"]
        else:
            self.link = None
        self.name = info["name"]
        # self.ds_path = info["ds_path"]
        # self.tb_path = info["tb_path"]
        
        self.port = info["port"]
        self.input_port,self.output_port = [],[]
        for port_name in self.port:
            if "in" in self.port[port_name][0]:
                self.input_port.append(port_name)
            else:
                self.output_port.append(port_name)

    def moduledef_gen(self):
        data = []
        if len(self.parameter) == 0:
            data.append("module {} (".format(self.name))
        else:
            data.append("module {} #(".format(self.name))
            param_list = ["\tparameter {} = {}".format(param,self.parameter[param][0]) for param in self.parameter]
            data.append(",\n".join(param_list))
            data.append(") (")
        port_list = []
        for p in self.port:
            port_info = self.port[p]
            if port_info[1] == "1":
                port_list.append("\t{} {}".format(port_info[0],p))
            else:
                port_list.append("\t{} [{} - 1 : 0] {}".format(port_info[0],port_info[1],p))
        data.append(",\n".join(port_list))
        data.append(");")
        return "\n".join(data)

    def instance_gen(self, inst_name, parent_param={}):
        inst = ["\n//instance {} module {}".format(inst_name,self.name)]
        # parameter generate
        for key in self.parameter:
            param_info = self.parameter[key]
            if parent_param.get(key) is not None:
                inst.append('parameter {}_{} = {};'.format(inst_name,key,key))
            else:
                inst.append('parameter {}_{} = {}; // cannot find,use default'.format(inst_name,key,param_info[0]))
                print("WARING:cannot find {}'parent paramter of {},use default".format(key,inst_name))
        # port generate
        for p in self.port:
            p_type,p_width,_ = self.port[p]
            tmp = "wire"
            if p_width.strip() != "1":
                if "`" not in p_width:
                    tmp += " [{}_{} - 1:0]".format(inst_name,p_width)
                else:
                    tmp += " [{} - 1:0]".format(p_width)
            tmp += " {}_{};".format(inst_name,p)
            inst.append(tmp)

        if len(self.parameter) == 0:
            inst.append("{} {} (".format(self.name,inst_name))
        else:
            inst.append("{} #(".format(self.name))
            param = ["\t.{}({}_{})".format(key,inst_name,key) for key in self.parameter]
            param = ",\n".join(param)
            inst.append(param)
            inst.append(") {} (".format(inst_name))

        port_text = ["\t.{}({}_{})".format(key,inst_name,key) for key in self.port]
        port_text = ",\n".join(port_text)
        inst.append(port_text)
        inst.append(");")
        return "\n".join(inst)

    def testbench_gen(self):
        pass

    def design_gen(self,link_text=""):
        pass

if __name__=='__main__':
    test = module_info("./example/info/test.json")
    # print(test.moduledef_gen())
    print(test.instance_gen("tse"))
    print(test.input_port)
    print(test.output_port)
