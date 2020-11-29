module test#(
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
	input [DWIDTH * PE_ROW​ - 1 : 0] outside_memory_din,
	output [DWIDTH * PE_ROW​ - 1 : 0] outside_memory_dout
);

//link inst_test_a
parameter inst_test_a_DWIDTH = DWIDTH;
wire inst_test_a_clk;
wire inst_test_a_rst_n;
wire inst_test_a_dout_valid;
wire [inst_test_a_DWIDTH - 1:0] inst_test_a_dout_data;
test_dout #(
	.DWIDTH(inst_test_a_DWIDTH)
) inst_test_a (
	.clk(inst_test_a_clk),
	.rst_n(inst_test_a_rst_n),
	.dout_valid(inst_test_a_dout_valid),
	.dout_data(inst_test_a_dout_data)
);

//link inst_test_b
parameter inst_test_b_DWIDTH = DWIDTH;
wire inst_test_b_clk;
wire inst_test_b_rst_n;
wire inst_test_b_din_valid;
wire [inst_test_b_DWIDTH - 1:0] inst_test_b_din_data;
test_din #(
	.DWIDTH(inst_test_b_DWIDTH)
) inst_test_b (
	.clk(inst_test_b_clk),
	.rst_n(inst_test_b_rst_n),
	.din_valid(inst_test_b_din_valid),
	.din_data(inst_test_b_din_data)
);

//link inst_test_c
parameter inst_test_c_DWIDTH = DWIDTH;
wire inst_test_c_clk;
wire inst_test_c_rst_n;
wire inst_test_c_din_valid;
wire [inst_test_c_DWIDTH - 1:0] inst_test_c_din_data;
test_din #(
	.DWIDTH(inst_test_c_DWIDTH)
) inst_test_c (
	.clk(inst_test_c_clk),
	.rst_n(inst_test_c_rst_n),
	.din_valid(inst_test_c_din_valid),
	.din_data(inst_test_c_din_data)
);
assign inst_test_b_din_valid = inst_test_a_dout_valid;
assign inst_test_b_din_data = inst_test_a_dout_data;
assign inst_test_c_din_valid = inst_test_a_dout_valid;
assign inst_test_c_din_data = inst_test_a_dout_data;
assign inst_test_a_clk = clk;
assign inst_test_a_rst_n = rst_n;
assign inst_test_b_clk = clk;
assign inst_test_b_rst_n = rst_n;
assign inst_test_c_clk = clk;
assign inst_test_c_rst_n = rst_n;

//progen-spilt:work after here


endmodule