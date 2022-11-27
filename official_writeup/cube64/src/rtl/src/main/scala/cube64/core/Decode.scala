package cube64.core

import chisel3._
import chisel3.util._
import cube64.config.CoreModule
import cube64.consts.Instructions

class Decode extends CoreModule {
  val io = IO(new Bundle {
    val inst = Input(UInt(instWidth.W))
    val stack0 = Input(UInt(dataWidth.W))
    val stack1 = Input(UInt(dataWidth.W))
    val sp = Input(UInt(spWidth.W))

    val newSp = Output(UInt(spWidth.W))
    val swap = Output(Bool())
    val opr1 = Output(UInt(dataWidth.W))
    val opr2 = Output(UInt(dataWidth.W))
    val aluOp = Output(UInt(aluOpWidth.W))
    val transfer = Output(Bool())
    val dir = Output(UInt(dirWidth.W))
    val lsuOp = Output(UInt(lsuOpWidth.W))
    val hasResult = Output(Bool())
    val out = Output(Bool())
    val halt = Output(Bool())
  })

  // control signals
  val (stackOp :: opr1 :: opr2 :: aluOp :: ctOp :: lsuOp ::
    (hasResult: Bool) :: (out: Bool) :: (halt: Bool) :: Nil) =
    ListLookup(io.inst, Instructions.DEFAULT, Instructions.TABLE)

  // stack operations
  val spOffset = MuxLookup(Cat(stackOp, hasResult), 0.U, Seq(
    Cat(Instructions.STACK_NULLARY, false.B) -> 0.U,
    Cat(Instructions.STACK_NULLARY, true.B) -> 1.U,
    Cat(Instructions.STACK_UNARY, false.B) -> -1.S(spWidth.W).asUInt,
    Cat(Instructions.STACK_UNARY, true.B) -> 0.U,
    Cat(Instructions.STACK_BINARY, false.B) -> -2.S(spWidth.W).asUInt,
    Cat(Instructions.STACK_BINARY, true.B) -> -1.S(spWidth.W).asUInt,
    Cat(Instructions.STACK_SWAP, false.B) -> 0.U,
  ))
  val newSp = io.sp + spOffset
  val swap = stackOp === Instructions.STACK_SWAP

  // operands
  val oprVal1 = readOpr(opr1)
  val oprVal2 = readOpr(opr2)
  def readOpr(oprSel: UInt) =
    MuxLookup(oprSel, 0.U, Seq(
      Instructions.OPR_STACK0 -> io.stack0,
      Instructions.OPR_STACK1 -> io.stack1,
      Instructions.OPR_ZERO -> 0.U,
      Instructions.OPR_ONE -> 1.U,
      Instructions.OPR_MAX -> -1.S(dataWidth.W).asUInt,
      Instructions.OPR_IMM -> io.inst(dataWidth - 1, 0),
    ))

  // flag of control transfer
  val transfer = MuxLookup(ctOp, false.B, Seq(
    Instructions.CT_NOP -> false.B,
    Instructions.CT_T -> oprVal1.orR,
    Instructions.CT_F -> !oprVal1.orR,
    Instructions.CT_J -> true.B,
  ))
  val dir = io.inst(dirWidth - 1, 0)

  // output
  io.newSp := RegNext(newSp)
  io.swap := RegNext(swap)
  io.opr1 := RegNext(oprVal1)
  io.opr2 := RegNext(oprVal2)
  io.aluOp := RegNext(aluOp)
  io.transfer := RegNext(transfer)
  io.dir := RegNext(dir)
  io.lsuOp := RegNext(lsuOp)
  io.hasResult := RegNext(hasResult)
  io.out := RegNext(out)
  io.halt := RegNext(halt)
}
