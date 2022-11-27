package cube64.mem

import chisel3._

class RomMasterIO(addrWidth: Int, dataWidth: Int) extends Bundle {
  val en = Output(Bool())
  val addr = Output(UInt(addrWidth.W))
  val readData = Input(UInt(dataWidth.W))
}

class Rom(addrWidth: Int, dataWidth: Int, content: Seq[Char]) extends Module {
  val io = IO(Flipped(new RomMasterIO(addrWidth, dataWidth)))
  val rom = RegInit(VecInit {
    content.iterator
      .concat(Iterator.continually(0.toChar))
      .take(1 << addrWidth)
      .map(_.U(dataWidth.W))
      .toSeq
  })
  io.readData := Mux(io.en, rom(io.addr), 0.U)
}
