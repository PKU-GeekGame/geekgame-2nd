package cube64

import chisel3._
import chisel3.stage.ChiselStage
import cube64.config.{CoreModule, HasCoreParams}
import cube64.core.{Core, WithDebugIO}
import cube64.mem.{Ram, Rom}

import scala.io.Source

class Cube64 extends CoreModule {
  class Cube64IO extends Bundle {
    val hasOutput = Output(Bool())
    val output = Output(UInt(dataWidth.W))
    val halt = Output(Bool())
  }

  class Cube64IOWithDebug extends Cube64IO with WithDebugIO

  val io = IO(if (enableDebug) new Cube64IOWithDebug else new Cube64IO)

  val romContent = Source.fromResource("rom.bin").toSeq
  val rom = Module(new Rom(romAddrWidth, instWidth, romContent))
  val ram = Module(new Ram(ramAddrWidth, dataWidth))
  val core = Module(new Core)
  core.io.rom <> rom.io
  core.io.ram <> ram.io
  io.hasOutput := core.io.hasOutput
  io.output := core.io.output
  io.halt := core.io.halt

  // debug output
  if (enableDebug) {
    val withDebug = io.asInstanceOf[WithDebugIO]
    withDebug.debug <> core.io.asInstanceOf[WithDebugIO].debug
  }
}

object Cube64 extends App {
  (new ChiselStage).emitVerilog(new Cube64)
}
