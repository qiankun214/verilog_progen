from data_structure import vfile_analysis,module_info
import argparse
import os

# get inport

# verilog analysis
def generate_testbench(input_path,output_path,module_name):
    analysiser = vfile_analysis(input_path)
    if module_name == "default":
        module_info = analysiser[0]
    else:
        for m in analysiser:
            if m.name == module_name:
                module_info = m
                break
        raise ValueError("ERROR:cannot find module {} in {}".format(module_name,input_path) )

    # testbench
    testbench_head = """

`timescale 1ns/1ps

module tb_{name} (); 

	logic rst_n;
	logic clk;

	// clock
	initial begin
		clk = '0;
		forever #(0.5) clk = ~clk;
	end

	// reset
	initial begin
		rst_n <= '0;
		#2
		rst_n <= '1;
	end

	// (*NOTE*) replace reset, clock, others
""".format(name = module_info.name)

    testbench_parameter = "\n".join(["\tparameter {} = {};".format(x,module_info.param_port[x]) for x in module_info.param_port])
    testbench_input_wire = "\n".join(["\tlogic {} {};".format(module_info.input_port[x],x) for x in module_info.input_port])
    testbench_output_wire = "\n".join(["\tlogic {} {};".format(module_info.output_port[x],x) for x in module_info.output_port])
    testbench_inst = module_info.inst("inst_{}".format(module_info.name))

    testbench_dump = """
    initial begin
        // testbench here
    end

	// dump wave
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

endmodule

""".format(name=module_info.name)

    testbench = "\n\n".join([testbench_head,testbench_parameter,testbench_input_wire,testbench_output_wire,testbench_inst,testbench_dump])

    # dump
    with open(output_path,'w') as f:
        f.write(testbench)
    print("Info:generate testbench in {}".format(output_path))

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help="input verilog file")
    parser.add_argument("-o", "--output", help="output systemverilog tb file",default="default")
    parser.add_argument("-m", "--module", help="module name",default="default")
    args = parser.parse_args()
    input_path = args.file
    if args.output == "default":
        root,path = os.path.split(input_path)
        name = os.path.splitext(path)[0]
        output_path = os.path.join(root,"tb_{}.sv".format(name))
    else:
        output_path = args.output
    module_name = args.module

    generate_testbench(input_path,output_path,module_name)