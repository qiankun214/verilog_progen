// pro-gen:start here,coding before this line
module tb_test_din ();

parameter DWIDTH = 16;

logic rst_n;
logic din_valid;
logic [DWIDTH - 1 : 0] din_data;
logic clk;

test_din #(
	.DWIDTH(DWIDTH)
) dut (
	.rst_n(rst_n),
	.din_valid(din_valid),
	.din_data(din_data),
	.clk(clk)
);

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

// pro-gen:stop here,coding after this line


endmodule