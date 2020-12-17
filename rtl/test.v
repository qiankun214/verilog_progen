
// pro-gen:start here,coding before this line
module test #(
	parameter PE_COL = 12,
	parameter PWIDTH = 4,
	parameter AWIDTH = 16,
	parameter DWIDTH = 16,
	parameter PE_ROW = 12,
	parameter OWIDTH = 8
) (
	input rst_n,
	input [POST_CWIDTH - 1 : 0] cfg_post_data,
	output [DWIDTH * PE_ROW - 1 : 0] outside_memory_dout,
	input clk,
	input cfg_valid,
	input [TMPC_CWIDTH - 1 : 0] cfg_tmpc_data,
	input [WICP_CWIDTH - 1 : 0] cfg_wicp_data,
	input [DWIDTH * PE_ROW - 1 : 0] outside_memory_din,
	input [DATA_CWIDTH - 1 : 0] cfg_data_data,
	input outside_memory_wreq,
	input [AWIDTH - 1 : 0] outside_memory_addr,
	output cfg_busy
);


//instance inst_test_b module test_din
parameter inst_test_b_DWIDTH = DWIDTH;
wire inst_test_b_rst_n;
wire [inst_test_b_DWIDTH - 1:0] inst_test_b_din_data;
wire inst_test_b_din_valid;
wire inst_test_b_clk;
test_din #(
	.DWIDTH(inst_test_b_DWIDTH)
) inst_test_b (
	.rst_n(inst_test_b_rst_n),
	.din_data(inst_test_b_din_data),
	.din_valid(inst_test_b_din_valid),
	.clk(inst_test_b_clk)
);

//instance inst_test_c module test_din
parameter inst_test_c_DWIDTH = DWIDTH;
wire inst_test_c_rst_n;
wire [inst_test_c_DWIDTH - 1:0] inst_test_c_din_data;
wire inst_test_c_din_valid;
wire inst_test_c_clk;
test_din #(
	.DWIDTH(inst_test_c_DWIDTH)
) inst_test_c (
	.rst_n(inst_test_c_rst_n),
	.din_data(inst_test_c_din_data),
	.din_valid(inst_test_c_din_valid),
	.clk(inst_test_c_clk)
);
// link
assign inst_test_b_clk = clk;
assign inst_test_c_clk = clk;
assign inst_test_b_rst_n = rst_n;
assign inst_test_c_rst_n = rst_n;
// this on link:
	// test.cfg_wicp_data
	//test.cfg_valid
	//inst_test_b.din_valid
	//test.cfg_busy
	//test.outside_memory_wreq
	//inst_test_c.din_valid
	//inst_test_c.din_data
	//test.cfg_data_data
	//test.outside_memory_addr
	//inst_test_b.din_data
	//test.outside_memory_din
	//test.cfg_tmpc_data
	//test.cfg_post_data
	//test.outside_memory_dout
// pro-gen:stop here,coding after this line
endmodule