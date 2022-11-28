# 扫雷 II

扫雷真是太好玩了，里面的雷各个都是雷才，boom又好听。

题目给了提示说理解去年的扫雷会有帮助，那基本确定从随机数函数下手。

### flag1

没写过go（此处鸣谢GoLand让我假装会写go了），但是看到`rand.Seed(time.Now().UnixMilli())`之后真实太开心了。
通常需要设置种子的随机数方法，只要种子确定后随机数都是一样的，因此只要找到种子就能得到后面生成的随机数了。

每次对游戏reset之后会将种子设置成收到请求时的毫秒数(`time.Now().UnixMilli()`)。
Chrome只能将发出请求的时间精确到秒，本来想自己写个更精确的记录时间的工具，但又转念一想，服务器的时钟跟自己电脑的时钟可能不一致，加上网络请求的耗时，记录精确时间没太大意义，还是增加一点搜索空间吧。

#### 解题步骤：

1. 开始游戏后点击一次reset，记录发出请求时的时间戳`ts`，单位毫秒。
2. 随便点击棋盘直到失败，记录结果。
3. 在`[ts - 500, ts + 1000]`的范围内设置随机数种子，检查生成的board与记录的网页board是否一致，若一致即找到了服务器用的种子，
4. 设置该种子之后再次获取的board即网页上当前的board。

### flag2

与flag1的路子大差不差，都是生成完整的board之后把结果腾挪到网页上。
难度的提升在于呈现board之前，执行了`rn`次`rand.Uint64()`，而`rn`是通过`securerand`生成的，生成过程应该没那么容易破解，这就引入了一个未知变量。
不过好在`rn`的取值范围最大不过255，搜索就是了。

由于执行`rn`次`rand.Uint64()`的过程有些耗时，可能需要将timestamp范围切片后多开几个进程同时搜索，还要记得搜索过程中每几分钟就去刷新一下网页，服务器中断了docker就白搜了。

### flag3

只要想清楚了flag3的board生成过程，解出的工作量应该大大小于flag2。
但是非科班出身的我对位运算的学习实在实在实在是太少了，导致第一阶段时候隐隐约约感觉到有点思路，但始终理不出头绪。第二阶段放出的提示我在第一阶段也已经都想到过，也就没帮上什么。

先说最终做出题的解法，再说中间走的一些弯路，还差一点点通过弯路解出了游戏。

#### 正常解

##### 1. 搜索seed过程

在`genBoard3()`中，`securerand`只控制了[1, 14]行的雷。
而第0行和第15行的雷是`rand.Intn()`控制的，虽然这两行当前位置周围的雷数未知，但是当前位置是不是雷是确定的。

因此可以通过第0和15行的board位置是不是雷来搜索seed，可能出现一局board搜索不出来seed的情况，就再开一局，两局总能确定一个seed。

##### 2. board计算过程

在`genBoard3()`中的两个数字`0x5554, 0x2aaa`的二进制形式都是...101010...，而我们知道（我是后知后觉）`0 & N = 0`，
因此二进制位是0的格子结果是确定的。

后面的代码又通过`rand.Intn()`生成的数字控制一个位置翻转或不翻转，在seed已知的情况下，`rand.Intn()`也是已知的。

所以最终生成的board的第1到14行，每隔一个格子就知道下一个格子是不是雷。
第0和第15行，又可以通过`rand.Intn()`直接算出是不是雷，剩下的交给脑子+不要发抖的手就能解出游戏了。

#### 我走的弯路

搜索过程如上，board计算过程出了很大问题。

由于开始时没想明白位运算的部分，只看出来`rand.Intn()`翻转位的部分是有规律的，
就通过运行1000次`genBoard3()`的方法将所有可能是雷的位置排除，最终剩下不可能是雷的board。

我用这个不可能是雷的board玩了一宿，最接近胜利的一次只差几个无解的格子就拿到flag，但是脸太黑，0.5的概率没有选对。

~~下次比赛前一定恶补计组知识~~

### 题目需要注意的点有

1. 自己电脑的时钟要精准，误差太大会影响搜索结果，赛方没有在服务器时钟上做手脚，不然这个题难度会陡然上升。
2. 设置seed之后，实际生成board的过程前和过程中究竟调用了多少次`random`要数清楚，不然永远得不到正确的board。

### 附件

#### flag2搜索过程的代码

```go
for k := timeMsec  - 500; k < timeMsec+4000; k++ {
    fmt.Printf("using Seed: %d\n", k)
    rand.Seed(k)

    var hugeMap = map[int][16]int{}
    
    randNum := int(rand.Uint64() % 20221119)

    for rn := randNum; rn < randNum+256; rn++ {

        rand.Seed(k)
        _ = int(rand.Uint64() % 20221119)

        for i := 0; i < rn; i += 1 {
            rand.Uint64()
        }

        var curBoard Board
        curBoard = genBoard2()

        hugeMap[rn] = curBoard
    }
}		
```

#### flag3计算board代码

```go
func printBoardDanger(mySeed int64, times int) {
	var board2D [16][16]int

	rand.Seed(mySeed)

	for j := 0; j < times; j++ {
		genBoard3()
	}

	for i := 0; i < 16; i++ {
		for j := 0; j < 16; j++ {
			temp := (rand.Intn(257)) % 2

			mask := 0x2aaa
			if i%2 == 0 {
				mask = 0x5554
			}
			if mask>>j&1 == 0 {
				board2D[i][j] = temp ^ 0
			} else {
				board2D[i][j] = -1
			}
		}
	}
	for i := 0; i < 16; i++ {
		for j := 0; j < 16; j++ {
			if board2D[i][j] == 1 {
				fmt.Printf(" * ")
			} else if board2D[i][j] == 0 {
				fmt.Printf(" 0 ")
			} else {
				fmt.Printf(" . ")
			}
		}
		println()
	}
}
```

#### flag3走弯路的代码

```go
func printBoardSafe(mySeed int64, times int, fullMarks [16]int) {

	var leastSquare [16][16]int
	for i := 0; i < 16; i++ {
		for j := 0; j < 16; j++ {
			leastSquare[i][j] = 0
		}
	}

	for i := 0; i < 1000; i++ {
		rand.Seed(mySeed)

		for j := 0; j < times; j++ {
			genBoard3()
		}

		result := showBoard(genBoard3(), fullMarks)

		for i := 0; i < 16; i++ {
			for j := 0; j < 16; j++ {
				if result[i][j] == -1 {
					leastSquare[i][j] = -1
				}
			}
		}
	}
	printResult(leastSquare)
}
```
