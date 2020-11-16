import json
import os

CLOCK_RSTN = """
wire auto_tb_clock,auto_tb_reset_n;
initial begin
    auto_tb_clock = 'b0;
    forever begin
        #5 auto_tb_clock = ~auto_tb_clock;
    end
end
initial begin
    auto_tb_reset_n = 'b0;
    #2 auto_tb_reset_n = 1'b1;
end
"""

FSDB = """
string dump_file;
initial begin
    `ifdef DUMP
        if($value$plusargs("FSDB=%s",dump_file))
            $display("dump_file = %s",dump_file);
        $fsdbDumpfile(dump_file);
        $fsdbDumpvars(0, tb_{name});
        $fsdbDumpMDA(0, tb_{name});
    `endif
end
"""

CLOCK_ASSIGN = """
// assign your clock and reset here
assign clk = auto_tb_clock;
assign rst_n = auto_tb_reset_n;
"""

class json2vsv(object):
    
    def __init__(self,js_path,ds_root,tb_root):
        super(json2vsv,self).__init__()
        self.info = self.js_load(js_path)
        self.name = self.info['name']
        self.ds_path,self.tb_path = self.path_gen(ds_root,tb_root)
        self.module_define = ""
        self.tb_define = ""

    def js_load(self,js_path):
        with open(js_path,'r') as f:
            data = json.load(f)
        return data

    def path_gen(self,ds_root,tb_root):
        ds = os.path.join(ds_root,"{}.v".format(self.name))
        tb = os.path.join(tb_root,"tb_{}.sv".format(self.name))
        return ds,tb

    def ds_generate(self):
        data = ["module {}".format(self.name),]
        if len(self.info['parameter']) == 0:
            data.append("(\n")
        else:
            data.append("#(\n")
            param_list = ["\tparameter {} = {}".format(param,self.info['parameter'][param][0]) for param in self.info['parameter']]
            data.append(",\n".join(param_list))
            data.append("\n) (\n")
        port_list = []
        for port in self.info['port']:
            port_info = self.info['port'][port]
            if port_info[1] == "1":
                port_list.append("\t{} {}".format(port_info[0],port))
            else:
                port_list.append("\t{} [{} - 1 : 0] {}".format(port_info[0],port_info[1],port))
        data.append(",\n".join(port_list))
        data.append("\n);\n\n{}\n// work here\n\nendmodule".format(self._link_generate()))
        self.module_define = "".join(data)

    def sv_generate(self):
        data = ["module tb_{} ();\n\n".format(self.name)]
        data += ["parameter {} = {};\n".format(x,self.info['parameter'][x][0]) for x in self.info['parameter']]
        data.append("\n")
        for port in self.info['port']:
            port_info = self.info['port'][port]
            if port_info[1] == "1":
                data.append("logic {};\n".format(port))
            else:
                data.append('logic [{} - 1 : 0] {};\n'.format(port_info[1],port))
        data.append("\n{} ".format(self.info['name']))
        if len(self.info['parameter']) == 0:
            data.append("dut (\n")
        else:
            data.append("#(\n")
            data.append(",\n".join(["\t.{}({})".format(x,x) for x in self.info['parameter']]))
            data.append("\n) dut (\n")
        data.append(",\n".join(["\t.{}({})".format(x,x) for x in self.info['port']]))
        data.append("\n);\n")
        data.append(CLOCK_RSTN)
        # data.append("\n")
        data.append(FSDB.format(name=self.name))
        data.append(CLOCK_ASSIGN)
        data.append("\n// your tb here\n\n\nendmodule")
        self.tb_define = "".join(data)

    def write(self):
        with open(self.ds_path,'w') as f:
            f.write(self.module_define)
        with open(self.tb_path,'w') as f:
            f.write(self.tb_define)

    def _link_generate(self):
        if self.info.get('link') is None:
            return
        link_list_big =  []
        for i in self.info['link']['link']:
            link_list_big += i
        link_text = [self._submodule_gen(key,self.info['link']['submodule'][key],link_list_big) for key in self.info['link']['submodule']]
        link_text.append(self._assign_net())
        return "\n\n".join(link_text)

    def _submodule_gen(self,name,minfo,link_list_big):
        submodule= []
        for key in minfo['parameter']:
            if self.info['parameter'].get(key) is not None:
                submodule.append('parameter {}_{} = {};'.format(name,key,key))
            else:
                submodule.append('parameter {}_{} = {};'.format(name,key,minfo['parameter'][key]))

        for port in minfo['port']:
            p_type,p_width = minfo['port'][port]
            tmp = "wire"
            if p_width.strip() != "1":
                tmp += " [{} - 1:0]".format(p_width)
            tmp += " {}_{};".format(name,port)
            if "{}.{}".format(name,port) not in link_list_big and self.info['port'].get(port) is not None:
                if "input" in p_type:
                    self.info['link']['link'].append(["{}_{}".format(name,port),port])
                else:
                    self.info['link']['link'].append([port,"{}_{}".format(name,port)])
            tmp += ";"
            submodule.append(tmp)

        if len(minfo['parameter']) == 0:
            submodule.append("{} {} (".format(minfo['module'],name))
        else:
            submodule.append("{} #(".format(minfo['module']))
            param = ["\t.{}({}_{})".format(key,name,key) for key in minfo['parameter']]
            param = ",\n".join(param)
            submodule.append(param)
            submodule.append(") {} (".format(name))

        port_text = ["\t.{}({}_{})".format(key,name,key) for key in minfo['port']]
        port_text = ",\n".join(port_text)
        submodule.append(port_text)
        submodule.append(");")
        return "\n".join(submodule)

    def _assign_net(self):
        result = []
        for p0,p1 in self.info['link']['link']:
            p0,p1 = p0.replace(".","_"),p1.replace(".","_")
            result.append("assign {} = {};".format(p0,p1))
        return "\n".join(result)

    def __call__(self):
        self.ds_generate()
        self.sv_generate()
        self.write()
        print("INFO:module '{}' rtl and tb generate finish".format(self.name))

if __name__ == "__main__":
    test = json2vsv("../doc/test.json","../doc","../doc")
    test()
