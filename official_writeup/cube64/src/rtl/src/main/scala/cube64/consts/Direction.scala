package cube64.consts

import chisel3._
import chisel3.util._

object Direction {
  val DIR_WIDTH = log2Ceil(6)
  val XP = 0.U(DIR_WIDTH.W)
  val XN = 1.U(DIR_WIDTH.W)
  val YP = 2.U(DIR_WIDTH.W)
  val YN = 3.U(DIR_WIDTH.W)
  val ZP = 4.U(DIR_WIDTH.W)
  val ZN = 5.U(DIR_WIDTH.W)
}
