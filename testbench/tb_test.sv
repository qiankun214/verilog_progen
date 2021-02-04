// pro-gen:start here,coding before this line
module tb_test ();

//instance dut module test
parameter dut_DWIDTH = 16; // cannot find,use default
parameter dut_AWIDTH = 16; // cannot find,use default
parameter dut_OWIDTH = 8; // cannot find,use default
parameter dut_PWIDTH = 4; // cannot find,use default
parameter dut_PE_ROW = 12; // cannot find,use default
parameter dut_PE_COL = 12; // cannot find,use default
logic dut_clk;
logic dut_rst_n;
logic dut_cfg_valid;
logic dut_cfg_busy;
logic [DATA_CWIDTH - 1:0] dut_cfg_data_data;
logic [WICP_CWIDTH - 1:0] dut_cfg_wicp_data;
logic [TMPC_CWIDTH - 1:0] dut_cfg_tmpc_data;
logic [POST_CWIDTH - 1:0] dut_cfg_post_data;
logic [dut_AWIDTH - 1:0] dut_outside_memory_addr;
logic dut_outside_memory_wreq;
logic [dut_DWIDTH * dut_PE_ROW - 1:0] dut_outside_memory_din;
logic [dut_DWIDTH * dut_PE_ROW - 1:0] dut_outside_memory_dout;
test #(
	.DWIDTH(dut_DWIDTH),
	.AWIDTH(dut_AWIDTH),
	.OWIDTH(dut_OWIDTH),
	.PWIDTH(dut_PWIDTH),
	.PE_ROW(dut_PE_ROW),
	.PE_COL(dut_PE_COL)
) dut (
	.clk(dut_clk),
	.rst_n(dut_rst_n),
	.cfg_valid(dut_cfg_valid),
	.cfg_busy(dut_cfg_busy),
	.cfg_data_data(dut_cfg_data_data),
	.cfg_wicp_data(dut_cfg_wicp_data),
	.cfg_tmpc_data(dut_cfg_tmpc_data),
	.cfg_post_data(dut_cfg_post_data),
	.outside_memory_addr(dut_outside_memory_addr),
	.outside_memory_wreq(dut_outside_memory_wreq),
	.outside_memory_din(dut_outside_memory_din),
	.outside_memory_dout(dut_outside_memory_dout)
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