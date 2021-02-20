// pro-gen:start here,coding before this line
interface port_dut #(
	parameter DWIDTH = 16,
	parameter AWIDTH = 16,
	parameter OWIDTH = 8,
	parameter PWIDTH = 4,
	parameter PE_ROW = 12,
	parameter PE_COL = 12
)(
	input clk,
	input rst_n
);
	logic cfg_valid;
	logic cfg_busy;
	logic [DATA_CWIDTH - 1:0] cfg_data_data;
	logic [WICP_CWIDTH - 1:0] cfg_wicp_data;
	logic [TMPC_CWIDTH - 1:0] cfg_tmpc_data;
	logic [POST_CWIDTH - 1:0] cfg_post_data;
	logic [AWIDTH - 1:0] outside_memory_addr;
	logic outside_memory_wreq;
	logic [DWIDTH * PE_ROW - 1:0] outside_memory_din;
	logic [DWIDTH * PE_ROW - 1:0] outside_memory_dout;

	// manage timing in clocking block like this
	clocking cb @(posedge clk);
		output cfg_valid;
		input cfg_busy;
		output cfg_data_data;
		output cfg_wicp_data;
		output cfg_tmpc_data;
		output cfg_post_data;
		output outside_memory_addr;
		output outside_memory_wreq;
		output outside_memory_din;
		input outside_memory_dout;
	endclocking
endinterface // port_dut

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

port_dut#(
	.DWIDTH(dut_DWIDTH),
	.AWIDTH(dut_AWIDTH),
	.OWIDTH(dut_OWIDTH),
	.PWIDTH(dut_PWIDTH),
	.PE_ROW(dut_PE_ROW),
	.PE_COL(dut_PE_COL)
) link_dut(dut_clk,dut_rst_n);
assign dut_cfg_valid = link_dut.cfg_valid;
assign link_dut.cfg_busy = dut_cfg_busy;
assign dut_cfg_data_data = link_dut.cfg_data_data;
assign dut_cfg_wicp_data = link_dut.cfg_wicp_data;
assign dut_cfg_tmpc_data = link_dut.cfg_tmpc_data;
assign dut_cfg_post_data = link_dut.cfg_post_data;
assign dut_outside_memory_addr = link_dut.outside_memory_addr;
assign dut_outside_memory_wreq = link_dut.outside_memory_wreq;
assign dut_outside_memory_din = link_dut.outside_memory_din;
assign link_dut.outside_memory_dout = dut_outside_memory_dout;

testbench_dut#(
	.DWIDTH(dut_DWIDTH),
	.AWIDTH(dut_AWIDTH),
	.OWIDTH(dut_OWIDTH),
	.PWIDTH(dut_PWIDTH),
	.PE_ROW(dut_PE_ROW),
	.PE_COL(dut_PE_COL)
) tb_dut (link_dut);
endmodule

program testbench_dut #(
	parameter DWIDTH = 16,
	parameter AWIDTH = 16,
	parameter OWIDTH = 8,
	parameter PWIDTH = 4,
	parameter PE_ROW = 12,
	parameter PE_COL = 12
) ( port_dut port );
// pro-gen:stop here,coding after this line

endprogram