// pro-gen:start here,coding before this line
module tb_test_dout ();

//instance dut module test_dout
parameter dut_DWIDTH = 16; // cannot find,use default
logic dut_rst_n;
logic dut_dout_valid;
logic dut_clk;
logic [dut_DWIDTH - 1:0] dut_dout_data;
test_dout #(
	.DWIDTH(dut_DWIDTH)
) dut (
	.rst_n(dut_rst_n),
	.dout_valid(dut_dout_valid),
	.clk(dut_clk),
	.dout_data(dut_dout_data)
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
        $fsdbDumpvars(0, tb_test_dout);
        $fsdbDumpMDA(0, tb_test_dout);
    `endif
end


// assign your clock and reset here
assign dut_clk = auto_tb_clock;
assign dut_rst_n = auto_tb_reset_n;

// pro-gen:stop here,coding after this line
endmodule