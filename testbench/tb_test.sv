// pro-gen:start here,coding before this line
module tb_test ();

//instance dut module test
parameter dut_PE_COL = 12; // cannot find,use default
parameter dut_PWIDTH = 4; // cannot find,use default
parameter dut_AWIDTH = 16; // cannot find,use default
parameter dut_DWIDTH = 16; // cannot find,use default
parameter dut_PE_ROW = 12; // cannot find,use default
parameter dut_OWIDTH = 8; // cannot find,use default
logic dut_rst_n;
logic [dut_POST_CWIDTH - 1:0] dut_cfg_post_data;
logic [dut_DWIDTH * PE_ROW - 1:0] dut_outside_memory_dout;
logic dut_clk;
logic dut_cfg_valid;
logic [dut_TMPC_CWIDTH - 1:0] dut_cfg_tmpc_data;
logic [dut_WICP_CWIDTH - 1:0] dut_cfg_wicp_data;
logic [dut_DWIDTH * PE_ROW - 1:0] dut_outside_memory_din;
logic [dut_DATA_CWIDTH - 1:0] dut_cfg_data_data;
logic dut_outside_memory_wreq;
logic [dut_AWIDTH - 1:0] dut_outside_memory_addr;
logic dut_cfg_busy;
test #(
	.PE_COL(dut_PE_COL),
	.PWIDTH(dut_PWIDTH),
	.AWIDTH(dut_AWIDTH),
	.DWIDTH(dut_DWIDTH),
	.PE_ROW(dut_PE_ROW),
	.OWIDTH(dut_OWIDTH)
) dut (
	.rst_n(dut_rst_n),
	.cfg_post_data(dut_cfg_post_data),
	.outside_memory_dout(dut_outside_memory_dout),
	.clk(dut_clk),
	.cfg_valid(dut_cfg_valid),
	.cfg_tmpc_data(dut_cfg_tmpc_data),
	.cfg_wicp_data(dut_cfg_wicp_data),
	.outside_memory_din(dut_outside_memory_din),
	.cfg_data_data(dut_cfg_data_data),
	.outside_memory_wreq(dut_outside_memory_wreq),
	.outside_memory_addr(dut_outside_memory_addr),
	.cfg_busy(dut_cfg_busy)
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
        $fsdbDumpvars(0, tb_test);
        $fsdbDumpMDA(0, tb_test);
    `endif
end


// assign your clock and reset here
assign dut_clk = auto_tb_clock;
assign dut_rst_n = auto_tb_reset_n;

// pro-gen:stop here,coding after this line
endmodule