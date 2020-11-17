module tb_test_dout ();

parameter DWIDTH = 16;

logic [DWIDTH - 1 : 0] dout_data;
logic dout_valid;
logic rst_n;
logic clk;

test_dout #(
	.DWIDTH(DWIDTH)
) dut (
	.dout_data(dout_data),
	.dout_valid(dout_valid),
	.rst_n(rst_n),
	.clk(clk)
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
assign clk = auto_tb_clock;
assign rst_n = auto_tb_reset_n;

//progen-spilt:work after here


endmodule