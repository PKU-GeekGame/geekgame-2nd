# Cube64 相关实现

该目录包含题目 “次世代立方计算机” 的相关源代码实现, 包括:

* `encrypt.py`: 核心 “加密算法” (劣化版 RC4) 的原型, 以及根据解密算法生成 Cube64 汇编的脚本.
* `assembler.py`: Cube64 汇编的汇编器.
* `disassembler.py`: Cube64 指令的反汇编器.
* `interpreter.py`: Cube64 指令的解释器. 该解释器具备输出 debug trace 的功能, 可用来调试 Cube64 的硬件实现.
* `rtl` 目录: Cube64 的硬件实现, 使用 Scala (Chisel) 编写. 该实现提供 debug 接口 (虽然没有启用), 可用于输出和 Cube64 指令解释器一致的 trace 信息.
* `sim` 目录: Cube64 的 Verilator 仿真顶层. 由于 Chisel Tester 的运行速度实在是太慢了, 我在实现硬件的过程中选用了 Verilator 跑仿真. 这个仿真顶层可以读取解释器输出的 debug trace, 和硬件的输出相对比, 从而尽可能快速定位硬件实现过程中的错误. 这种思想叫做 [“差分测试”](https://en.wikipedia.org/wiki/Differential_testing), 而且确实帮我快速定位了一些因疏忽导致的错误.

如果你对 `sim` 目录中的 Verilator 顶层感兴趣, 你可以:

先将 `rtl/src/main/scala/cube64/config/HasCoreParams.scala` 中 27 行的 `enableDebug` 设为 `true`, 然后安装 `sbt`, 在 `rtl` 目录内执行:

```
sbt run
```

此时会输出 `Cube64.v`. 然后安装 `verilator`, 执行:

```
verilator --cc --exe --trace-fst --build ../sim/sim.cpp Cube64.v
```

此时会生成 `obj_dir/VCube64`, 即为编译后的 Cube64 仿真程序.

需要注意的是, 在仿真程序中, `Ram` 的内容是清零的. 为了得到完全一致的 debug trace, 你可以注释掉 `interpreter.py` 中的 347-350 行, 然后执行:

```
./interpreter.py rom.bin debug.trace
```

此时会输出 debug trace. 然后你可以执行:

```
obj_dir/VCube64 debug.trace
```

此时仿真程序会对对 Cube64 进行仿真, 同时比较 debug trace, 尽可能确保在此过程中硬件的行为和解释器的行为一致.

此外, 仿真程序还会收集仿真过程中 Cube64 内的所有信号, 将其输出为 FST 格式的波形文件, 保存在 `trace.fst` 中, 你可以使用 GTKWave 等软件查看.
