package cube64.mem

import chisel3._
import chisel3.util._

class StackControlIO(spWidth: Int, dataWidth: Int) extends Bundle {
  val writeEn = Bool()
  val writeSp = UInt(spWidth.W)
  val writeDataEn = Bool()
  val writeData = UInt(dataWidth.W)
  val swap = Bool()
}

class Stack(width: Int, depth: Int) extends Module {
  require(isPow2(depth))
  val SP_WIDTH = log2Ceil(depth)

  val io = IO(new Bundle {
    val control = Input(new StackControlIO(SP_WIDTH, width))
    val stack0 = Output(UInt(width.W))
    val stack1 = Output(UInt(width.W))
    val sp = Output(UInt(SP_WIDTH.W))
  })

  val stack = RegInit(VecInit(Seq.fill(depth) {
    0.U(width.W)
  }))
  val sp = RegInit(0.U(SP_WIDTH.W))
  val sp2 = sp - 1.U

  when(io.control.writeEn) {
    sp := io.control.writeSp
    when(io.control.writeDataEn) {
      stack(io.control.writeSp) := io.control.writeData
    }
  }.elsewhen(io.control.swap) {
    stack(sp) := io.stack1
    stack(sp2) := io.stack0
  }

  io.stack0 := stack(sp)
  io.stack1 := stack(sp2)
  io.sp := sp
}
