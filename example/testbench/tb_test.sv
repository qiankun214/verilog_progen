// pro-gen:start here,coding before this line
module tb_test ();

parameter PE_COL = 12;
parameter PE_ROW = 12;
parameter AWIDTH = 16;
parameter DWIDTH = 16;
parameter PWIDTH = 4;
parameter OWIDTH = 8;

logic [DATA_CWIDTH - 1 : 0] cfg_data_data;
logic [DWIDTH * PE_ROW​ - 1 : 0] outside_memory_dout;
logic cfg_valid;
logic [AWIDTH - 1 : 0] outside_memory_addr;
logic cfg_busy;
logic clk;
logic outside_memory_wreq;
logic [TMPC_CWIDTH - 1 : 0] cfg_tmpc_data;
logic [DWIDTH * PE_ROW​ - 1 : 0] outside_memory_din;
logic rst_n;
logic [POST_CWIDTH - 1 : 0] cfg_post_data;
logic [WICP_CWIDTH - 1 : 0] cfg_wicp_data;

test #(
	.PE_COL(PE_COL),
	.PE_ROW(PE_ROW),
	.AWIDTH(AWIDTH),
	.DWIDTH(DWIDTH),
	.PWIDTH(PWIDTH),
	.OWIDTH(OWIDTH)
) dut (
	.cfg_data_data(cfg_data_data),
	.outside_memory_dout(outside_memory_dout),
	.cfg_valid(cfg_valid),
	.outside_memory_addr(outside_memory_addr),
	.cfg_busy(cfg_busy),
	.clk(clk),
	.outside_memory_wreq(outside_memory_wreq),
	.cfg_tmpc_data(cfg_tmpc_data),
	.outside_memory_din(outside_memory_din),
	.rst_n(rst_n),
	.cfg_post_data(cfg_post_data),
	.cfg_wicp_data(cfg_wicp_data)
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
assign clk = auto_tb_clock;
assign rst_n = auto_tb_reset_n;

// pro-gen:stop here,coding after this line


endmodule