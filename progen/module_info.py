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
        self.link = info["link"]
        self.name = info["name"]
        self.submodule = info["submodule"]
        self.port = info["port"]
        self.input_port,self.output_port = [],[]
        for port_name in self.port:
            if "in" in self.port[port_name][0]:
                self.input_port.append(port_name)
            else:
                self.output_port.append(port_name)
        self.tb_path = info["tb_path"]
        self.ds_path = info["ds_path"]
        self.unlink = info["unlink"]
        self.dependent = info["dependent"]

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
        # print(data)
        return "\n".join(data)

    def instance_gen(self, inst_name, parent_param={},net_type="wire"):
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
            tmp = net_type
            if p_width.strip() != "1":
                if "`" in p_width or p_width.isdigit():
                    tmp += " [{} - 1:0]".format(p_width)
                else:
                    tmp += " [{}_{} - 1:0]".format(inst_name,p_width)
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

    def link_generate(self):
        result,un_result = [],""
        for ip,op in self.link:
            ip,op = ip.split("."),op.split(".")
            if ip[0] == self.name:
                ip = [ip[1],]
            if op[0] == self.name:
                op = [op[1],]
            result.append("assign {} = {};".format("_".join(ip),"_".join(op)))
        un_result = "// this on link:\n\t// {}".format("\n\t//".join(self.unlink))
        return "\n".join(result),un_result

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
