package cube64.config

import chisel3.util._
import cube64.consts.{Direction, Instructions}

trait HasCoreParams {
  // memory/RAM parameters
  val dataWidth = 6
  val ramAddrWidth = 6

  // ROM parameters
  val posWidth = 4
  val romAddrWidth = 3 * posWidth
  val instWidth = Instructions.INST_WIDTH

  // stack parameters
  val stackDepth = 32
  require(isPow2(stackDepth))
  val spWidth = log2Ceil(stackDepth)

  // function unit parameters
  val aluOpWidth = Instructions.ALU_WIDTH
  val dirWidth = Direction.DIR_WIDTH
  val lsuOpWidth = Instructions.LSU_WIDTH

  // debug parameters
  val enableDebug = false
}
