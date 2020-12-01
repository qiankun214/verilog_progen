from os import name
from module_info import module_info
import os

LINE_START = "// pro-gen:start here,coding before this line"
LINE_STOP = "// pro-gen:stop here,coding after this line"
CLOCK_RSTN = """
logic auto_tb_clock,auto_tb_reset_n;
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
assign dut_clk = auto_tb_clock;
assign dut_rst_n = auto_tb_reset_n;
"""
class ds_generator(object):

    def __init__(self,info,info_root="./info"):
        super(ds_generator,self).__init__()
        self.info = info 
        self.content = ""
        self.info_root = info_root
        self.initial_content = "{}\n{}\nendmodule"

    def get_content(self,ds_path,is_use=True):
        if is_use and os.path.exists(ds_path):
            with open(ds_path,'r') as f:
                data = f.read().split("\n")
                self.content = self._spilt_content(data)
        else:
            print("INFO:cannot find {} or define noupdate,write new".format(ds_path))
            self.content = self.initial_content
            return
        
    def _spilt_content(self,data):
        result,flag = [],True
        for line in data:
            if LINE_START in line:
                flag = False
                result.append('{}')
            elif LINE_STOP in line:
                flag = True
                continue

            if flag and len(line.strip()) != 0:
                result.append(line)
        return "\n".join(result)
    
    def get_submodule_link(self):
        link = [LINE_START]
        for inst in self.info.submodule:
            module = self.info.submodule[inst]
            subm_info_path = os.path.join(self.info_root,"{}.json".format(module))
            subm_info = module_info(subm_info_path)
            link.append(subm_info.instance_gen(inst,self.info.parameter))
        link.append("// link")
        line_link,line_unlink = self.info.link_generate()
        link.append(line_link)
        link.append(line_unlink)
        link.append(LINE_STOP)
        link.append("\n")
        # print(link)
        return "\n".join(link)

    def get_module_def(self):
        m_def = [
            LINE_START,
            self.info.moduledef_gen(),
            LINE_STOP,"\n"
        ]
        return "\n".join(m_def)

    def write_ds(self):
        with open(self.info.ds_path,'w') as f:
            f.write(self.content.format(
                self.get_module_def(),
                self.get_submodule_link()
            ))

    def __call__(self,is_use):
        self.get_content(self.info.ds_path,is_use)
        # print(self.content)
        self.write_ds()

class tb_generator(ds_generator):

    def __init__(self,info,info_root="./info"):
        super(tb_generator,self).__init__(info,info_root)
        tmp = "module tb_{} ();".format(self.info.name)
        self.initial_content = "\n".join([
            "module tb_{} ();".format(self.info.name),
            "{}",
            "",
            "endmodule"
        ])

    def __call__(self,is_use):
        self.get_content(self.info.tb_path,is_use)
        tmp = "\n".join([
            LINE_START,
            self.info.instance_gen("dut"),
            CLOCK_RSTN,
            FSDB.format(name=self.info.name),
            CLOCK_ASSIGN,
            LINE_STOP
        ])
        with open(self.info.tb_path,'w') as f:
            f.write(self.content.format(tmp))


