package cube64.core

import chisel3._
import cube64.config.HasCoreParams
import cube64.mem.StackControlIO

class DebugIO extends Bundle with HasCoreParams {
  val stack = new StackControlIO(spWidth, dataWidth)
}

trait WithDebugIO {
  val debug = Output(new DebugIO)
}
