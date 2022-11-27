package cube64

import chiseltest._
import chiseltest.simulator.WriteVcdAnnotation
import org.scalatest.flatspec.AnyFlatSpec

import scala.collection.mutable.ArrayBuffer

class Cube64Test extends AnyFlatSpec with ChiselScalatestTester {
  behavior of "Cube64"
  it should "output the flag" in {
    test(new Cube64).withAnnotations(Seq(WriteVcdAnnotation)) { c =>
      val out = ArrayBuffer[Int]()
      var i = 0
      while (!c.io.halt.peekBoolean()) {
        i += 1
        c.clock.step()
        if (c.io.hasOutput.peekBoolean()) {
          out += c.io.output.peekInt().toInt
          print(s"cycle: $i, output: ${c.io.output.peekInt()}, ")
          println(s"output length: ${out.length}")
        }
      }
      println("====================")
      println(s"final output: ${out.mkString("[", ", ", "]")}")
      println(s"output length: ${out.length}")
    }
  }
}
