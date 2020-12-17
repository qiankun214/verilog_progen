// pro-gen:start here,coding before this line
module tb_test_din ();

//instance dut module test_din
parameter dut_DWIDTH = 16; // cannot find,use default
logic dut_rst_n;
logic dut_din_valid;
logic dut_clk;
logic [dut_DWIDTH - 1:0] dut_din_data;
test_din #(
	.DWIDTH(dut_DWIDTH)
) dut (
	.rst_n(dut_rst_n),
	.din_valid(dut_din_valid),
	.clk(dut_clk),
	.din_data(dut_din_data)
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
assign dut_clk = auto_tb_clock;
assign dut_rst_n = auto_tb_reset_n;

// pro-gen:stop here,coding after this line
endmodule