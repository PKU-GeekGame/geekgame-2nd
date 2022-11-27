package cube64.core

import chisel3._
import chisel3.util._
import cube64.config.{CoreModule, HasCoreParams}
import cube64.mem.{RamMasterIO, RomMasterIO, Stack}


class Core extends CoreModule {
  class CoreIO extends Bundle {
    val rom = new RomMasterIO(romAddrWidth, instWidth)
    val ram = new RamMasterIO(ramAddrWidth, dataWidth)
    val hasOutput = Output(Bool())
    val output = Output(UInt(dataWidth.W))
    val halt = Output(Bool())
  }

  class CoreIOWithDebug extends CoreIO with WithDebugIO

  val io = IO(if (enableDebug) new CoreIOWithDebug else new CoreIO)

  // FSM
  val sFetch :: sDecode :: sExecute :: Nil = Enum(3)
  val state = RegInit(sFetch)
  state :=
    Mux(state === sFetch, sDecode,
    Mux(state === sDecode, sExecute, sFetch))

  // stack
  val stack = Module(new Stack(dataWidth, stackDepth))

  // fetch
  val fetch = Module(new Fetch)
  fetch.io.en := state === sFetch
  fetch.io.rom <> io.rom

  // decode
  val decode = Module(new Decode)
  decode.io.inst := fetch.io.inst
  decode.io.stack0 := stack.io.stack0
  decode.io.stack1 := stack.io.stack1
  decode.io.sp := stack.io.sp

  // execute
  val execute = Module(new Execute)
  execute.io.en := state === sExecute
  execute.io.newSp := decode.io.newSp
  execute.io.swap := decode.io.swap
  execute.io.opr1 := decode.io.opr1
  execute.io.opr2 := decode.io.opr2
  execute.io.aluOp := decode.io.aluOp
  execute.io.transfer := decode.io.transfer
  execute.io.dir := decode.io.dir
  execute.io.lsuOp := decode.io.lsuOp
  execute.io.hasResult := decode.io.hasResult
  stack.io.control <> execute.io.stackControl
  fetch.io.dirEn := execute.io.dirEn
  fetch.io.dir := execute.io.newDir
  execute.io.ram <> io.ram

  // flags
  io.hasOutput := decode.io.out
  io.output := Mux(decode.io.out, decode.io.opr1, 0.U)
  io.halt := decode.io.halt

  // debug output
  if (enableDebug) {
    val withDebug = io.asInstanceOf[WithDebugIO]
    withDebug.debug.stack <> execute.io.stackControl
  }
}
