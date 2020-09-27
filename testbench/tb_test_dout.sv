module tb_test_dout ();

parameter DWIDTH = 16;

logic clk;
logic rst_n;
logic dout_valid;
logic [DWIDTH - 1 : 0] dout_data;

test_dout #(
	.DWIDTH(DWIDTH)
) dut (
	.clk(clk),
	.rst_n(rst_n),
	.dout_valid(dout_valid),
	.dout_data(dout_data)
);

wire auto_tb_clock,auto_tb_reset_n;
inital begin
    auto_tb_clock = 'b0;
    forever begin
        #5 auto_tb_clock = ~auto_tb_clock;
    end
end
inital begin
    auto_tb_reset_n = 'b0;
    #2 auto_tb_reset_n = 1'b1;
end

string dump_file;
initial begin
    `ifdef DUMP
        if($value$plusargs("FSDB=%s",dump_file))
            $display("dump_file = %s",dump_file);
        $fsdbDumpfile(dump_file);
        $fsdbDumpvars(0, tb_test_dout);
        $fsdbDumpMDA(0, tb_test_dout);
    `endif
end

// assign your clock and reset here
assign clk = auto_tb_clock;
assign rst_n = auto_tb_reset_n;

// your tb here


endmodule