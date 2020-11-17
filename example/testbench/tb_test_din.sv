module tb_test_din ();

parameter DWIDTH = 16;

logic din_valid;
logic clk;
logic rst_n;
logic [DWIDTH - 1 : 0] din_data;

test_din #(
	.DWIDTH(DWIDTH)
) dut (
	.din_valid(din_valid),
	.clk(clk),
	.rst_n(rst_n),
	.din_data(din_data)
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
        $fsdbDumpvars(0, tb_test_din);
        $fsdbDumpMDA(0, tb_test_din);
    `endif
end

// assign your clock and reset here
assign clk = auto_tb_clock;
assign rst_n = auto_tb_reset_n;

// your tb here


endmodule