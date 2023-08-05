module TOP(CLK, RST, IN, IN2, reg1, OUT);
  input CLK, RST, IN, IN2;
  reg reg1,reg3;
  output reg1,OUT;
  wire in1;

  always @(posedge CLK or negedge RST) begin
    if(RST) begin
      reg1 <= 1'b0;
    end else begin
      reg1 <= IN;
    end
  end

  SUB sub(CLK,RST,in1,OUT);
endmodule

