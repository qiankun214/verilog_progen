// pro-gen:start here,coding before this line
module test#(
	parameter PE_COL = 12,
	parameter PE_ROW = 12,
	parameter AWIDTH = 16,
	parameter DWIDTH = 16,
	parameter PWIDTH = 4,
	parameter OWIDTH = 8
) (
	input [DATA_CWIDTH - 1 : 0] cfg_data_data,
	output [DWIDTH * PE_ROW​ - 1 : 0] outside_memory_dout,
	input cfg_valid,
	input [AWIDTH - 1 : 0] outside_memory_addr,
	output cfg_busy,
	input clk,
	input outside_memory_wreq,
	input [TMPC_CWIDTH - 1 : 0] cfg_tmpc_data,
	input [DWIDTH * PE_ROW​ - 1 : 0] outside_memory_din,
	input rst_n,
	input [POST_CWIDTH - 1 : 0] cfg_post_data,
	input [WICP_CWIDTH - 1 : 0] cfg_wicp_data
);

//link inst_test_a
parameter inst_test_a_DWIDTH = DWIDTH;
wire inst_test_a_rst_n;
wire inst_test_a_clk;
wire inst_test_a_dout_valid;
wire [inst_test_a_DWIDTH - 1:0] inst_test_a_dout_data;
test_dout #(
	.DWIDTH(inst_test_a_DWIDTH)
) inst_test_a (
	.rst_n(inst_test_a_rst_n),
	.clk(inst_test_a_clk),
	.dout_valid(inst_test_a_dout_valid),
	.dout_data(inst_test_a_dout_data)
);

//link inst_test_b
parameter inst_test_b_DWIDTH = DWIDTH;
wire [inst_test_b_DWIDTH - 1:0] inst_test_b_din_data;
wire inst_test_b_rst_n;
wire inst_test_b_clk;
wire inst_test_b_din_valid;
test_din #(
	.DWIDTH(inst_test_b_DWIDTH)
) inst_test_b (
	.din_data(inst_test_b_din_data),
	.rst_n(inst_test_b_rst_n),
	.clk(inst_test_b_clk),
	.din_valid(inst_test_b_din_valid)
);

//link inst_test_c
parameter inst_test_c_DWIDTH = DWIDTH;
wire [inst_test_c_DWIDTH - 1:0] inst_test_c_din_data;
wire inst_test_c_rst_n;
wire inst_test_c_clk;
wire inst_test_c_din_valid;
test_din #(
	.DWIDTH(inst_test_c_DWIDTH)
) inst_test_c (
	.din_data(inst_test_c_din_data),
	.rst_n(inst_test_c_rst_n),
	.clk(inst_test_c_clk),
	.din_valid(inst_test_c_din_valid)
);
assign inst_test_b_din_valid = inst_test_a_dout_valid;
assign inst_test_b_din_data = inst_test_a_dout_data;
assign inst_test_c_din_valid = inst_test_a_dout_valid;
assign inst_test_c_din_data = inst_test_a_dout_data;
assign inst_test_a_rst_n = rst_n;
assign inst_test_a_clk = clk;
assign inst_test_b_rst_n = rst_n;
assign inst_test_b_clk = clk;
assign inst_test_c_rst_n = rst_n;
assign inst_test_c_clk = clk;

// pro-gen:stop here,coding after this line


endmodule