package cube64.core

import chisel3._
import chisel3.util._
import cube64.config.CoreModule
import cube64.consts.{Direction, Instructions}
import cube64.mem.RomMasterIO

class Fetch extends CoreModule {
  val io = IO(new Bundle {
    val en = Input(Bool())
    val dirEn = Input(Bool())
    val dir = Input(UInt(dirWidth.W))
    val inst = Output(UInt(instWidth.W))

    // ROM interface
    val rom = new RomMasterIO(romAddrWidth, instWidth)
  })

  // direction
  val dir = RegInit(Direction.XP)
  val nextDir = Mux(io.dirEn, io.dir, dir)
  when (io.en) { dir := nextDir }

  // position
  val (x, nextX) = pos(-1.S(posWidth.W).asUInt, Direction.XP, Direction.XN)
  val (y, nextY) = pos(0.U(posWidth.W), Direction.YP, Direction.YN)
  val (z, nextZ) = pos(0.U(posWidth.W), Direction.ZP, Direction.ZN)
  def pos(init: UInt, dirPos: UInt, dirNeg: UInt) = {
    val p = RegInit(init)
    val next =
      Mux(nextDir === dirPos, p + 1.U,
      Mux(nextDir === dirNeg, p - 1.U, p))
    when (io.en) { p := next }
    (p, next)
  }

  // fetch the current instruction from the ROM
  val pc = Cat(nextZ, nextY, nextX)
  io.rom.en := io.en
  io.rom.addr := pc
  io.inst := RegNext(io.rom.readData)
}
