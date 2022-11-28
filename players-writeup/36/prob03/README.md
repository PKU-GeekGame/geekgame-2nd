# 智慧检测器

## Flag 1

阅读[源码](./src.py)之后发现两处问题：

```py
    DisplayData.append(map[z][0])
    for i in range(1, len(map[z]) - 1):
        DisplayData.append([map[z][i][0]] + [" "]*(size-2) + [map[z][i][-1]])
    DisplayData.append(map[z][-1])
```

```py
                CurPos = NewPos
                if map[CurPos[0]][CurPos[1]][CurPos[2]] == "E":
                    print("Congratulations! You finished within %d moves." %
                          MoveCount)
                    FoundEnd = True
                    break
```

这两处都犯了没有对 `list` 进行深拷贝的错误。利用第二处错误，可以在走了一个合法操作之后再多走一步；利用第一处错误，可以将第一行和最后一行的 `#` 修改为 `@`。下面给出一个利用这两处错误的例子：

```txt
#######
#@    #
# XXX #
#     #
# X   #
#     #
####E##
Input direction and press enter. Available directions: SE R(estart)
SSSSS
Invalid Direction
#######
#     #
#     #
#     #
# X   #
# X   #
#@##E##
Input direction and press enter. Available directions: N R(estart)
NSS
Invalid Direction
got <class 'IndexError'>
flag{game.exe-stops-respondiNg...sEnd-ERror-report?}
```

可以看到，在第一个操作序列（最后一步不合法）后，我们成功地移动到了最后一行上，并且此时最后一行第二格的 `#` 被永久修改为了 `@`。之后我们再进行一个类似的操作序列（最后一步不合法），就成功地将 `CurPos` 修改为了越界值，之后就会触发 `IndexError`，从而得到 Flag 1。

## Flag 2

利用获得 Flag 1 所用到的观察玩游戏通关即可。

几个要点：

- 首先进行一次 `XD`（`X` 为任意合法操作）看一下最后一层的 `E` 在哪里，这决定了我们后面行进的方向。如果距离太远（对角线），也可以考虑重开。
- `R` 重开（因为 `XD` 之后当前高度变为 `-1`，无法移动）
- 利用 `XU` 向上走。如果遇到 `T`，可以碰碰运气，也许可以节约很多步数。
- 到达最后一层后，走到 `E` 即可。注意中间尽可能用 `XY`（`Y` 为任意非法操作）的方式节约步数。

尝试几次之后成功通关。

```txt
Congratulations! You finished within 89 moves.
flag{Dear-player-thanks-for-enJoyIng-this-ubisoft-gaMe}
```
