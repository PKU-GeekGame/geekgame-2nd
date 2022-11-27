package cube64.mem

import chisel3._

class RamMasterIO(addrWidth: Int, dataWidth: Int) extends Bundle {
  val en = Output(Bool())
  val writeEn = Output(Bool())
  val addr = Output(UInt(addrWidth.W))
  val writeData = Output(UInt(dataWidth.W))
  val readData = Input(UInt(dataWidth.W))
}

class Ram(addrWidth: Int, dataWidth: Int) extends Module {
  val io = IO(Flipped(new RamMasterIO(addrWidth, dataWidth)))

  val mem = Mem(1 << addrWidth, UInt(dataWidth.W))

  io.readData := DontCare
  when (io.en) {
    when (io.writeEn) {
      mem.write(io.addr, io.writeData)
    } .otherwise {
      io.readData := mem.read(io.addr)
    }
  }
}
