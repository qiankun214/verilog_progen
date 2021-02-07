
// pro-gen:start here,coding before this line
module test #(
	parameter DWIDTH = 16,
	parameter AWIDTH = 16,
	parameter OWIDTH = 8,
	parameter PWIDTH = 4,
	parameter PE_ROW = 12,
	parameter PE_COL = 12
) (
	input clk,
	input rst_n,
	input cfg_valid,
	output cfg_busy,
	input [DATA_CWIDTH - 1 : 0] cfg_data_data,
	input [WICP_CWIDTH - 1 : 0] cfg_wicp_data,
	input [TMPC_CWIDTH - 1 : 0] cfg_tmpc_data,
	input [POST_CWIDTH - 1 : 0] cfg_post_data,
	input [AWIDTH - 1 : 0] outside_memory_addr,
	input outside_memory_wreq,
	input [DWIDTH * PE_ROW - 1 : 0] outside_memory_din,
	output [DWIDTH * PE_ROW - 1 : 0] outside_memory_dout
);


//instance inst_test_b module test_din
parameter inst_test_b_DWIDTH = DWIDTH;
wire inst_test_b_clk;
wire inst_test_b_rst_n;
wire inst_test_b_din_valid;
wire [2 * inst_test_b_DWIDTH + 3 - 1:0] inst_test_b_din_data;
test_din #(
	.DWIDTH(inst_test_b_DWIDTH)
) inst_test_b (
	.clk(inst_test_b_clk),
	.rst_n(inst_test_b_rst_n),
	.din_valid(inst_test_b_din_valid),
	.din_data(inst_test_b_din_data)
);

//instance inst_test_c module test_din
parameter inst_test_c_DWIDTH = DWIDTH;
wire inst_test_c_clk;
wire inst_test_c_rst_n;
wire inst_test_c_din_valid;
wire [2 * inst_test_c_DWIDTH + 3 - 1:0] inst_test_c_din_data;
test_din #(
	.DWIDTH(inst_test_c_DWIDTH)
) inst_test_c (
	.clk(inst_test_c_clk),
	.rst_n(inst_test_c_rst_n),
	.din_valid(inst_test_c_din_valid),
	.din_data(inst_test_c_din_data)
);
// link
assign inst_test_b_clk = clk;
assign inst_test_c_clk = clk;
assign inst_test_b_rst_n = rst_n;
assign inst_test_c_rst_n = rst_n;
// this on link:
	// test.cfg_post_data
	//inst_test_c.din_valid
	//inst_test_b.din_valid
	//test.outside_memory_wreq
	//test.outside_memory_din
	//inst_test_b.din_data
	//test.cfg_tmpc_data
	//inst_test_c.din_data
	//test.cfg_valid
	//test.cfg_wicp_data
	//test.cfg_busy
	//test.cfg_data_data
	//test.outside_memory_dout
	//test.outside_memory_addr
// pro-gen:stop here,coding after this line
endmodule