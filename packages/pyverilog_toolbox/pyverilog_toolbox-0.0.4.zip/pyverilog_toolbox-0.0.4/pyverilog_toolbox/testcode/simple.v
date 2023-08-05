module TOP(CLK);
  input CLK;
  reg A,B;
  reg C;

  always @(posedge CLK) begin
    A <= 1'b1;
    B <= 1'b0;
  end

  always @(posedge CLK) begin
    C <= 1'b1;
  end

  SUB sub(CLK);
endmodule

module SUB(CLK);
  input CLK;
endmodule

