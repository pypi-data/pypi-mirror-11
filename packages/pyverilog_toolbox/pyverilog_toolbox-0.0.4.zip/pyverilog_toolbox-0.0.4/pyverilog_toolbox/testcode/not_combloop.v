module TOP(CLK, RSTN);
  input CLK,RSTN;
  reg reg1;

  always @(posedge CLK or negedge RSTN) begin
    if(!RSTN) begin
      reg1 <= 0;
    end else begin
      reg1 <= reg1;
    end
  end

endmodule

