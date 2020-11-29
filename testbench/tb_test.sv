module tb_test ();

parameter DWIDTH = 16;
parameter AWIDTH = 16;
parameter OWIDTH = 8;
parameter PWIDTH = 4;
parameter PE_ROW = 12;
parameter PE_COL = 12;

logic clk;
logic rst_n;
logic cfg_valid;
logic cfg_busy;
logic [DATA_CWIDTH - 1 : 0] cfg_data_data;
logic [WICP_CWIDTH - 1 : 0] cfg_wicp_data;
logic [TMPC_CWIDTH - 1 : 0] cfg_tmpc_data;
logic [POST_CWIDTH - 1 : 0] cfg_post_data;
logic [AWIDTH - 1 : 0] outside_memory_addr;
logic outside_memory_wreq;
logic [DWIDTH * PE_ROW​ - 1 : 0] outside_memory_din;
logic [DWIDTH * PE_ROW​ - 1 : 0] outside_memory_dout;

test #(
	.DWIDTH(DWIDTH),
	.AWIDTH(AWIDTH),
	.OWIDTH(OWIDTH),
	.PWIDTH(PWIDTH),
	.PE_ROW(PE_ROW),
	.PE_COL(PE_COL)
) dut (
	.clk(clk),
	.rst_n(rst_n),
	.cfg_valid(cfg_valid),
	.cfg_busy(cfg_busy),
	.cfg_data_data(cfg_data_data),
	.cfg_wicp_data(cfg_wicp_data),
	.cfg_tmpc_data(cfg_tmpc_data),
	.cfg_post_data(cfg_post_data),
	.outside_memory_addr(outside_memory_addr),
	.outside_memory_wreq(outside_memory_wreq),
	.outside_memory_din(outside_memory_din),
	.outside_memory_dout(outside_memory_dout)
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

//progen-spilt:work after here


endmodule