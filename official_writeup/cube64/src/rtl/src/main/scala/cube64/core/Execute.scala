package cube64.core

import chisel3._
import chisel3.util._
import cube64.config.CoreModule
import cube64.consts.Instructions
import cube64.mem.{RamMasterIO, StackControlIO}

class Execute extends CoreModule {
  val io = IO(new Bundle {
    val en = Input(Bool())
    val newSp = Input(UInt(spWidth.W))
    val swap = Input(Bool())
    val opr1 = Input(UInt(dataWidth.W))
    val opr2 = Input(UInt(dataWidth.W))
    val aluOp = Input(UInt(aluOpWidth.W))
    val transfer = Input(Bool())
    val dir = Input(UInt(dirWidth.W))
    val lsuOp = Input(UInt(lsuOpWidth.W))
    val hasResult = Input(Bool())

    // to stack
    val stackControl = Output(new StackControlIO(spWidth, dataWidth))

    // to fetch
    val dirEn = Output(Bool())
    val newDir = Output(UInt(dirWidth.W))

    // to RAM
    val ram = new RamMasterIO(ramAddrWidth, dataWidth)
  })

  // ALU
  val shiftAmount = io.opr2(2, 0)
  val aluResult = MuxLookup(io.aluOp, 0.U, Seq(
    Instructions.ALU_ADD -> (io.opr1 + io.opr2),
    Instructions.ALU_SUB -> (io.opr1 - io.opr2),
    Instructions.ALU_AND -> (io.opr1 & io.opr2),
    Instructions.ALU_OR -> (io.opr1 | io.opr2),
    Instructions.ALU_XOR -> (io.opr1 ^ io.opr2),
    Instructions.ALU_SHL -> (io.opr1 << shiftAmount).asUInt,
    Instructions.ALU_SHR -> (io.opr1 >> shiftAmount).asUInt,
    Instructions.ALU_SAR -> (io.opr1.asSInt >> shiftAmount).asUInt,
    Instructions.ALU_LT -> (io.opr1.asSInt < io.opr2.asSInt).asUInt,
    Instructions.ALU_LTU -> (io.opr1 < io.opr2).asUInt,
    Instructions.ALU_EQ -> (io.opr1 === io.opr2).asUInt,
  ))

  // load and store
  val ramEn = io.en && io.lsuOp =/= Instructions.LSU_NOP
  val ramWriteEn = io.lsuOp === Instructions.LSU_ST
  val ramAddr = io.opr1
  val ramWriteData = io.opr2
  val lsuResult = io.ram.readData

  // final result
  val result = Mux(ramEn, lsuResult, aluResult)

  // to stack
  io.stackControl.writeEn := RegNext(io.en && !io.swap)
  io.stackControl.writeSp := RegNext(io.newSp)
  io.stackControl.writeDataEn := RegNext(io.hasResult)
  io.stackControl.writeData := RegNext(result)
  io.stackControl.swap := RegNext(io.en && io.swap)

  // to fetch
  io.dirEn := RegNext(io.transfer)
  io.newDir := RegNext(io.dir)

  // to RAM
  io.ram.en := ramEn
  io.ram.writeEn := ramWriteEn
  io.ram.addr := ramAddr
  io.ram.writeData := ramWriteData
}
