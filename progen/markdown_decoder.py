import json
import os
# from os import SEEK_SET, path
# markdown_decoder(path,info_root) : read -> spilt -> decode parameter 
# -> decode port -> decode inst -> decode link -> link -> write json

class source_decoder(object):

    def __init__(self):
        super(source_decoder,self).__init__()

    def table_handle(self,table):
        result = []
        for line in table:
            if "|" in line:
                this_data = [x.strip() for x in line.split("|")[1:-1]]
                # print(this_data)
                if len(this_data[0]) == this_data[0].count("-"):
                    if len(result) == 0:
                        raise ValueError("FATAL:error when decode {}".format(line))
                    result = result[:-1]
                    continue
                result.append(this_data)
        return result

    def decode(self,content):
        raise ValueError("decode not implement")

class parameter_decoder(source_decoder):

    def __init__(self):
        super(parameter_decoder,self).__init__()

    def decode(self,content):
        parameter_list = self.table_handle(content)
        result = {}
        for name,comment,defaultnum in parameter_list:
            if result.get(name) is not None:
                raise ValueError("FATAL:parameter {} is mult define".format(name))
            result[name] = [defaultnum,comment]
        return result

class port_decoder(source_decoder):
    
    def __init__(self):
        super(port_decoder,self).__init__()

    def decode(self, content):
        port_list = self.table_handle(content)
        result = {}
        for name,dtype,width,comment in port_list:
            if result.get(name) is not None:
                raise ValueError("FATAL:port {} is mult define")
            result[name] = [dtype,width,comment]
        return result

class dependent_decoder(source_decoder):
    
    def __init__(self):
        super(dependent_decoder,self).__init__()

    def decode(self, content):
        result = []
        for line in content:
            l = line.strip()
            if len(l) == 0:
                continue
            if l[0] == "-":
                dependent = l[1:].strip()
                if not os.path.exists(dependent):
                    raise ValueError("FATAL:dependent file {} not exists".format(dependent))
                result.append(dependent)
        return result

class link_decoder(source_decoder):

    def __init__(self):
        super(link_decoder,self).__init__()

    def decode(self, content):
        submodule_list = self.table_handle(content)
        result_sub,result_link = {},self._link_decoder(content)
        for inst,module in submodule_list:
            result_sub[inst] = module
        return result_sub,result_link
        
    def _link_decoder(self,content):
        result = []
        for line in content:
            if len(line) == 0:
                continue
            if line[0] == "-":
                this_link = [x.strip() for x in line[1:].split("<>")]
                result.append(this_link)
        return result

class markdown_decoder(object):

    def __init__(self):
        self.name = None
        self.path = None

        self.d_port = port_decoder()
        self.d_param = parameter_decoder()
        self.d_link = link_decoder()
        self.d_depen = dependent_decoder()

        self.c_port = ""
        self.c_param = ""
        self.c_link = ""
        self.c_depen = ""
        self.c_othre = []

        self.port = None
        self.param = None
        self.submodule = None
        self.dependent = None
        self.link = None

        self.add_link = []

        self.ds_path = ""
        self.tb_path = ""
        self.unlink = []

    def _get_name(self,path):
        md_name = os.path.split(path)[-1]
        self.name = os.path.splitext(md_name)[0]
        self.path = path

    def spilt_markdown(self,path):
        self._get_name(path)
        with open(path,'r',encoding='utf-8') as f:
            content = f.read().strip()
        content = "\n{}".format(content.replace("\u200b",""))
        content_list = [x.split("\n") for x in content.split("\n# ")]
        for i,part in enumerate(content_list[1:]):
            head = part[0].strip()
            self.c_othre.append("# {}".format(head))
            self.c_othre += part[1:]
            if head == "port":
                self.c_port = part
            elif head == "parameter":
                self.c_param = part
            elif head == "dependent":
                self.c_depen = part
            elif head == "link":
                self.c_link = part
                self.c_othre[-1] += "{link}"

    def decode(self):
        self.port = self.d_port.decode(self.c_port)
        self.param = self.d_param.decode(self.c_param)
        self.submodule,self.link = self.d_link.decode(self.c_link)
        self.dependent = self.d_depen.decode(self.c_depen)

    def add_link_gen(self,request):
        self.add_link = request

    def assgin_ds_path(self,root):
        self.ds_path = os.path.join(root,"{}.v".format(self.name)) 

    def assgin_tb_path(self,root):
        self.tb_path = os.path.join(root,"tb_{}.sv".format(self.name))

    def assgin_unlink(self,unlink):
        self.unlink = unlink

    def renew_link(self,link):
        self.link = link

    def save_info(self,root):
        path = os.path.join(root,"{}.json".format(self.name))
        info = {
            "name":self.name,
            "port":self.port,
            "parameter":self.param,
            "dependent":self.dependent,
            "submodule":self.submodule,
            "link":self.link,
            "unlink":self.unlink,
            "ds_path":self.ds_path,
            "tb_path":self.tb_path
        }
        with open(path,'w') as f:
            json.dump(info,f,indent=4)

    def save_md(self):
        content = "\n".join(self.c_othre)
        alink = ["- {} <> {}".format(*x) for x in self.add_link]
        if len(alink) != 0:
            alink = ["\n> this is generate by linker",] + alink + ["",]
            alink = "\n".join(alink)
            content = content.format(link=alink)
        else:
            content = content.format(link="")
        with open(self.path,'w') as f:
            f.write(content)

if __name__ == "__main__":
    d = markdown_decoder()
    d.spilt_markdown("./inputs/test.md")
    d.decode()
    print("\n".join(d.c_othre))
