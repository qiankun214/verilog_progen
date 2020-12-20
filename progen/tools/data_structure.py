
import re
import os
# from graphviz import Digraph

class module_info(object):
    """docstring for module_info"""
    def __init__(self):
        super(module_info, self).__init__()
        self.name = None
        self.path = None
        self.content = ""
        self.submodule_list = {}
        self.submodule_content = {}
        self.submodule = []
        self.input_port = {}
        self.output_port = {}
        self.param_port = {}

    def __str__(self):
        return "%s(%s)" % (self.name,self.path)

    def inst(self,inst_name):
        # print(self.param_port)
        if len(self.param_port) == 0:
            head = "{} {} (".format(self.name,inst_name)
        else:
            head = "{} #(".format(self.name)
            param = ",\n".join(["\t.{name}({name})".format(name=x) for x in self.param_port])
            head = "\n".join([head,param,") {} (".format(inst_name)])
        input_str =  ["\t.{name}({name})".format(name=x) for x in self.input_port]
        output_str = ["\t.{name}({name})".format(name=x) for x in self.output_port]	
        port = ",\n".join(input_str + output_str)
        return "\n".join([head,port,");"])

class vfile_analysis(object):
    """docstring for vfile_analysis"""
    def __init__(self,path):
        super(vfile_analysis, self).__init__()
        self.verilog = ("module","case","if","for","generate","endgenerate","forever")
        self.path = path
        self.result = []
        with open(path,'r') as f:
            self.content = f.read()
        self._remove_annotation()
        self._find_module()
        for name in self.content:
            m_info = module_info()
            m_info.name = name
            m_info.path = path
            m_info.content = self.content[name]
            m_info.input_port,m_info.output_port = self._anaylsis_port(self.content[name])
            m_info.param_port = self._anaylsis_parameter(self.content[name])
            for subcontent,submodule,subname in self._find_submodule(name):
                if m_info.submodule_list.get(submodule) is None:
                    m_info.submodule_list[submodule] = [subname]
                    m_info.submodule_content[submodule] = [subcontent]
                else:
                    m_info.submodule_list[submodule].append(subname)
                    m_info.submodule_content[submodule].append(subcontent)

            self.result.append(m_info)
        print("Info:%s analysis finish" % path)

    def _remove_annotation(self):
        self.content = re.sub(r"//.*\n","\n",self.content)
        self.content = re.sub(r"/\*[\s\S]*?\*/","",self.content)

    def _find_module(self):
        m = re.findall(r"(module\s+(\w+)[\s\S]*?endmodule)",self.content)
        if len(m) == 0:
            print("Error,cannot find module in file %s" % self.path)
        self.content = dict([x[::-1] for x in m])

    def _find_submodule(self,mname):
        data = self.content[mname]
        m = re.findall(r"(\n\s*(\w+)[ \f\r\t\v]+(\w+)\s*\([\s\S]*?\);)",data)
        m += re.findall(r"(\n\s*(\w+)[ \f\r\t\v]*#\([\S\s]*?\)\s*(\w+)\s*\([\s\S]*?\);)",data)
        # print(m)
        m = [list(x) for x in m if x[2] not in self.verilog and x[1] not in self.verilog]
        for i in m:
            i[0] = i[0].strip()
            i[0] = re.sub(r"\n\s*","",i[0])
            # print("Info:find submodule %s which inst name %s in module %s" % (i[1],i[2],mname))
        return m

    def _anaylsis_port(self,content):
        input_port_list = re.findall(r"input\s*(\[.*?:.*?\]+)*\s*(\w+)",content)
        input_port_dict = dict([x[::-1] for x in input_port_list])			
        output_port_list = re.findall(r"output\s*(reg)*\s*(\[.*?:.*?\])*\s*(\w+)",content)
        output_port_dict = dict([(x[-1],x[-2]) for x in output_port_list])
        return input_port_dict,output_port_dict

    def _anaylsis_parameter(self,content):
        parameter_define_content = re.search(r"#\([\s\S]+?\)",content)
        if parameter_define_content is not None:
            parameter_define_content = parameter_define_content.group(0)
            parameter_list = re.findall(r"parameter\s+(\w+)\s*=\s*(.*)\,*",parameter_define_content)
            return dict([(x[0],x[1].replace(",","")) for x in parameter_list])
        return {}

    def __getitem__(self,x):
        return self.result[x]

    def __len__(self):
        return len(self.result)

class struct_analysis(object):
    """docstring for struct_analysis"""
    def __init__(self,root,avoid=" "):
        super(struct_analysis, self).__init__()
        self.root = root
        self.avoid = avoid
        self.file_list = [os.path.join(self.root,x) for x in os.listdir(self.root) if x[-2:] == ".v"]
        self._file_analysis()
        self._generate_tree()
        for m in self.root_node:
            self._debug_print(m)
        # self.draw_dot("./data.png")

    def _file_analysis(self):
        self.module_list = []
        for path in self.file_list:
            self.module_list += vfile_analysis(path)

    def _generate_tree(self):
        self.root_node = []
        for m in self.module_list:
            flag = 0
            for i in self.module_list:
                if i.submodule_list.get(m.name) is not None:
                    flag = 1
                    i.submodule.append(m)
            if flag == 0 and self.avoid not in m.name:
                self.root_node.append(m)
                # print("find root %s" % m.name)
        # print([x.name for x in self.root_node])
        # print(len(self.module_list),len(self.root_node))

    def _debug_print(self,node,pre=""):
        print("%s%s" % (pre,node))
        for x in node.submodule:
            self._debug_print(x,"\t"+pre)

    # def draw_dot(self,output_path,target_file=None):
    #     dot = Digraph(filename=output_path)
    #     if target_file is None:
    #         for m in self.root_node:
    #             self._sub_draw(dot,m,None)
    #     else:
    #         for m in self.root_node:
    #             if m.name == target_file:
    #                 self._sub_draw(dot,m,None)
    #                 return
    #         raise ValueError("FATAL no root {}".format(target_file))
    #     dot.render('{}.gv'.format(target_file), view=True)

    # def _sub_draw(self,dot,node,pre=None):
    #     dot.node(str(node),str(node))
    #     if pre is not None:
    #         dot.edge(str(pre),str(node))
    #     for x in node.submodule:
    #         self._sub_draw(dot,x,node)
