import os
import json
from module_info import module_info
# from module_info.module_info

class linker(object):

    def __init__(self,parent):
        super(linker,self).__init__()
        self.port_list = {}
        self.no_link_port = set()
        self.parent = parent
        self.assgin_result = []

    def port_append(self,inst_name,port_list):
        for port in port_list:
            ptype,width,comment = port_list[port]
            if self.port_list.get(port) is None:
                self.port_list[port] = {}
            if inst_name != self.parent:
                self.port_list[port][inst_name] = [ptype,width,comment]
            elif "output" in ptype:
                self.port_list[port][inst_name] = ["input",width,comment]
            elif "input" in ptype:
                self.port_list[port][inst_name] = ["output",width,comment]
            self.no_link_port.add("{}.{}".format(inst_name,port))
    # {'port name':['inst1','inst2']}

    def generate_assign(self,request):
        port1_inst,port1_name,port2_inst,port2_name = self._get_port(request)
        # print(self.no_link_port)
        if "{}.{}".format(port1_inst,port1_name) in self.no_link_port:
            self.no_link_port.remove("{}.{}".format(port1_inst,port1_name))
        if "{}.{}".format(port2_inst,port2_name) in self.no_link_port:
            self.no_link_port.remove("{}.{}".format(port2_inst,port2_name))
        result = ["{}.{}".format(port1_inst,port1_name),"{}.{}".format(port2_inst,port2_name)]
        self.assgin_result.append(result)

    def check_unlink(self):
        result = []
        for name in self.no_link_port.copy():
            if name not in self.no_link_port:
                continue
            port,inst,info = self._get_unlink(name)
            if "output" in info[0]:
                continue
            print("\nWARING:{}.{} not connet,you need choose net to link or link manual".format(inst,port))
            switch_list = self.switch_link_target(port,info[0],inst)
            for i,vinfo in enumerate(switch_list):
                print("{}). {}.{}({}):{}".format(i,vinfo[0],port,vinfo[2],vinfo[3]))
            din = input("you can input index / inst.port / press enter(later link manual):").strip()
            if len(din) == 0:
                continue
            elif din.isdigit():
                if int(din) >= len(switch_list):
                    print("WARING:{} cannot switch,default use manual".format(din))
                    continue
                target = switch_list[int(din)]
                self.generate_assign(["{}.{}".format(inst,port),"{}.{}".format(target[0],port)])
                result.append(["{}.{}".format(inst,port),"{}.{}".format(target[0],port)])
            else:
                self.generate_assign(["{}.{}".format(inst,port),din])
                result.append(["{}.{}".format(inst,port),din])
        print("WARING:you should link manul:")
        for name in self.no_link_port:
            print("\t{}".format(name))
        return result

    def switch_link_target(self,port_name,port_type,port_inst):
        if "input" in port_type:
            target_type = "output"
        else:
            target_type = "input"
        
        result = []
        for inst in self.port_list[port_name]:
            vinfo = self.port_list[port_name][inst]
            if inst == port_inst or target_type not in vinfo[0]:
                continue
            result.append([inst,] + vinfo)
        # print(self.port_list[port_name],port_name)
        return result

    def _get_unlink(self,name):
        if "." in name:
            inst,port = name.split(".")
        else:
            inst,port = self.parent,name
        return port,inst,self.port_list[port][inst]

    def _get_port(self,request):
        assert len(request) == 2
        port1,port2 = request

        # spilt
        if "." in port1:
            inst1,port1 = port1.strip().split(".")
            is_parent = False
        else:
            inst1 = self.parent
            is_parent = True

        if "." in port2:
            inst2,port2 = port2.strip().split(".")
            is_parent = False
        else:
            inst2 = self.parent
            if is_parent:
                raise ValueError("FATAL:request {} not need".format(request))
            else:
                is_parent = True

        # get info
        if self.port_list.get(port1) is not None:
            if self.port_list[port1].get(inst1) is not None:
                info1 = self.port_list[port1][inst1]
            else:
                raise ValueError("FATAL:port {} not exists in {}".format(port1,inst1))
        else:
            raise ValueError("FATAL:port {} not exists".format(port1))

        if self.port_list.get(port2) is not None:
            if self.port_list[port2].get(inst2) is not None:
                info2 = self.port_list[port2][inst2]
            else:
                raise ValueError("FATAL:port {} not exists in inst {}".format(port2, inst2))
        else:
            raise ValueError("FATAL:port {} not exists".format(port2))

        # check
        if "input" in info1[0] and "input" in info2[0]:
            raise ValueError("FATAL:(both input)link port type no match,{}.{}({}) not match {}.{}({})".format(
                inst1,port1,info1[1],inst2,port2,info2[1]
            ))
        if "output" in info1[0] and "output" in info2[0]:
            raise ValueError("FATAL:(both output)link port type no match,{}.{}({}) not match {}.{}({})".format(
                inst1,port1,info1[1],inst2,port2,info2[1]
            ))
        # if is_parent and "input" in info1[0] and "input" not in info2[0]:
        #     raise ValueError("FATAL:link port type no match,{}.{}({}) not match {}.{}({})".format(
        #         inst1,port1,info1[1],inst2,port2,info2[1]
        #     ))
        # if is_parent and "output" in info1[0] and "output" in info2[0]:
        #     raise ValueError("FATAL:link port type no match,{}.{}({}) not match {}.{}({})".format(
        #         inst1,port1,info1[1],inst2,port2,info2[1]
        #     ))
        if info1[1] != info2[1]:
            print("WARING:link port width not match,{}.{}({}) not match {}.{}({})".format(
                inst1,port1,info1[1],inst2,port2,info2[1]
            ))        
        if "input" in info1[0]:
            return inst1,port1,inst2,port2
        return inst2,port2,inst1,port1

class markdown_link(object):

    def __init__(self,mk_decoder,info_root):
        super(markdown_link,self).__init__()
        self.markdown = mk_decoder
        self.linker = linker(self.markdown.name)
        self.linker.port_append(self.markdown.name,self.markdown.port)
        self.root = info_root
        self.final_link = []
        self.add_link = []
        self.unlink = []

    def analysis_submodule(self):
        for inst in self.markdown.submodule:
            module = self.markdown.submodule[inst]
            minfo = self._info_read(module)
            self.linker.port_append(inst,minfo.port)

    def _info_read(self,module):
        path = os.path.join(self.root,"{}.json".format(module))
        return module_info(path)

    def scan_link(self):
        for l in self.markdown.link:
            self.linker.generate_assign(l)
        self.add_link = self.linker.check_unlink()
        self.final_link = self.linker.assgin_result
        self.unlink = list(self.linker.no_link_port)

    def __call__(self):
        self.analysis_submodule()
        # print(self.linker.port_list)
        self.scan_link()
        return self.final_link,self.add_link,self.unlink