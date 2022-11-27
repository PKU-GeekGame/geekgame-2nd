package cube64.consts

import chisel3._
import chisel3.util._

object Instructions {
  // instructions
  val INST_WIDTH = 7
  val INST_NOP = "b0000000".U(INST_WIDTH.W)

  // patterns
  val NOP = BitPat("b0000000")
  val DUP = BitPat("b0000001")
  val SWAP = BitPat("b0000010")
  val LD = BitPat("b0000011")
  val ST = BitPat("b0000100")
  val OUT = BitPat("b0000101")
  val HALT = BitPat("b0000110")
  val INC = BitPat("b0000111")
  val ADD = BitPat("b0001000")
  val SUB = BitPat("b0001001")
  val AND = BitPat("b0001010")
  val OR = BitPat("b0001011")
  val NOT = BitPat("b0001100")
  val XOR = BitPat("b0001101")
  val SHL = BitPat("b0001110")
  val SHR = BitPat("b0001111")
  val SAR = BitPat("b0010000")
  val LT = BitPat("b0010001")
  val LTU = BitPat("b0010010")
  val EQ = BitPat("b0010011")
  val BT = BitPat("b0100???")
  val BF = BitPat("b0101???")
  val J = BitPat("b0110???")
  val LI = BitPat("b1??????")

  // true/false
  val Y = true.B
  val N = false.B

  // stack operation
  val STACK_WIDTH = log2Ceil(4)
  val STACK_NULLARY = 0.U(STACK_WIDTH.W)
  val STACK_UNARY = 1.U(STACK_WIDTH.W)
  val STACK_BINARY = 2.U(STACK_WIDTH.W)
  val STACK_SWAP = 3.U(STACK_WIDTH.W)

  // operand selector
  val OPR_WIDTH = log2Ceil(6)
  val OPR_STACK0 = 0.U(OPR_WIDTH.W)
  val OPR_STACK1 = 1.U(OPR_WIDTH.W)
  val OPR_ZERO = 2.U(OPR_WIDTH.W)
  val OPR_ONE = 3.U(OPR_WIDTH.W)
  val OPR_MAX = 4.U(OPR_WIDTH.W)
  val OPR_IMM = 5.U(OPR_WIDTH.W)

  // ALU operation
  val ALU_WIDTH = log2Ceil(11)
  val ALU_ADD = 0.U(ALU_WIDTH.W)
  val ALU_SUB = 1.U(ALU_WIDTH.W)
  val ALU_AND = 2.U(ALU_WIDTH.W)
  val ALU_OR = 3.U(ALU_WIDTH.W)
  val ALU_XOR = 4.U(ALU_WIDTH.W)
  val ALU_SHL = 5.U(ALU_WIDTH.W)
  val ALU_SHR = 6.U(ALU_WIDTH.W)
  val ALU_SAR = 7.U(ALU_WIDTH.W)
  val ALU_LT = 8.U(ALU_WIDTH.W)
  val ALU_LTU = 9.U(ALU_WIDTH.W)
  val ALU_EQ = 10.U(ALU_WIDTH.W)

  // control transfer operation
  val CT_WIDTH = log2Ceil(4)
  val CT_NOP = 0.U(CT_WIDTH.W)
  val CT_T = 1.U(CT_WIDTH.W)
  val CT_F = 2.U(CT_WIDTH.W)
  val CT_J = 3.U(CT_WIDTH.W)

  // LSU operation
  val LSU_WIDTH = log2Ceil(3)
  val LSU_NOP = 0.U(LSU_WIDTH.W)
  val LSU_LD = 1.U(LSU_WIDTH.W)
  val LSU_ST = 2.U(LSU_WIDTH.W)

  // @formatter:off
  // decode table
  val DEFAULT =
  //                                                                         hasResult halt
  //               stackOp        opr1        opr2       aluOp   ctOp     lsuOp   | out |
  //                  |            |           |           |       |        |     |  |  |
            List(STACK_NULLARY, OPR_ZERO,   OPR_ZERO,   ALU_ADD, CT_NOP, LSU_NOP, N, N, N)
  val TABLE = Array(
    NOP  -> List(STACK_NULLARY, OPR_ZERO,   OPR_ZERO,   ALU_ADD, CT_NOP, LSU_NOP, N, N, N),
    DUP  -> List(STACK_NULLARY, OPR_STACK0, OPR_ZERO,   ALU_ADD, CT_NOP, LSU_NOP, Y, N, N),
    SWAP -> List(STACK_SWAP,    OPR_ZERO,   OPR_ZERO,   ALU_ADD, CT_NOP, LSU_NOP, N, N, N),
    LD   -> List(STACK_UNARY,   OPR_STACK0, OPR_ZERO,   ALU_ADD, CT_NOP, LSU_LD,  Y, N, N),
    ST   -> List(STACK_BINARY,  OPR_STACK0, OPR_STACK1, ALU_ADD, CT_NOP, LSU_ST,  N, N, N),
    OUT  -> List(STACK_UNARY,   OPR_STACK0, OPR_ZERO,   ALU_ADD, CT_NOP, LSU_NOP, N, Y, N),
    HALT -> List(STACK_NULLARY, OPR_ZERO,   OPR_ZERO,   ALU_ADD, CT_NOP, LSU_NOP, N, N, Y),
    INC  -> List(STACK_UNARY,   OPR_STACK0, OPR_ONE,    ALU_ADD, CT_NOP, LSU_NOP, Y, N, N),
    ADD  -> List(STACK_BINARY,  OPR_STACK1, OPR_STACK0, ALU_ADD, CT_NOP, LSU_NOP, Y, N, N),
    SUB  -> List(STACK_BINARY,  OPR_STACK1, OPR_STACK0, ALU_SUB, CT_NOP, LSU_NOP, Y, N, N),
    AND  -> List(STACK_BINARY,  OPR_STACK1, OPR_STACK0, ALU_AND, CT_NOP, LSU_NOP, Y, N, N),
    OR   -> List(STACK_BINARY,  OPR_STACK1, OPR_STACK0, ALU_OR,  CT_NOP, LSU_NOP, Y, N, N),
    NOT  -> List(STACK_UNARY,   OPR_STACK0, OPR_MAX,    ALU_XOR, CT_NOP, LSU_NOP, Y, N, N),
    XOR  -> List(STACK_BINARY,  OPR_STACK1, OPR_STACK0, ALU_XOR, CT_NOP, LSU_NOP, Y, N, N),
    SHL  -> List(STACK_BINARY,  OPR_STACK1, OPR_STACK0, ALU_SHL, CT_NOP, LSU_NOP, Y, N, N),
    SHR  -> List(STACK_BINARY,  OPR_STACK1, OPR_STACK0, ALU_SHR, CT_NOP, LSU_NOP, Y, N, N),
    SAR  -> List(STACK_BINARY,  OPR_STACK1, OPR_STACK0, ALU_SAR, CT_NOP, LSU_NOP, Y, N, N),
    LT   -> List(STACK_BINARY,  OPR_STACK1, OPR_STACK0, ALU_LT,  CT_NOP, LSU_NOP, Y, N, N),
    LTU  -> List(STACK_BINARY,  OPR_STACK1, OPR_STACK0, ALU_LTU, CT_NOP, LSU_NOP, Y, N, N),
    EQ   -> List(STACK_BINARY,  OPR_STACK1, OPR_STACK0, ALU_EQ,  CT_NOP, LSU_NOP, Y, N, N),
    BT   -> List(STACK_UNARY,   OPR_STACK0, OPR_ZERO,   ALU_ADD, CT_T,   LSU_NOP, N, N, N),
    BF   -> List(STACK_UNARY,   OPR_STACK0, OPR_ZERO,   ALU_ADD, CT_F,   LSU_NOP, N, N, N),
    J    -> List(STACK_NULLARY, OPR_ZERO,   OPR_ZERO,   ALU_ADD, CT_J,   LSU_NOP, N, N, N),
    LI   -> List(STACK_NULLARY, OPR_IMM,    OPR_ZERO,   ALU_ADD, CT_NOP, LSU_NOP, Y, N, N),
  )
  // @formatter:on
}
