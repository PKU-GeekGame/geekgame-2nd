# 智慧检测器

## 解题过程
先尝试手玩，尝试各种违规操作。发现如果给一串指令，如果第一步合法，第二步就可以穿墙。在迷宫边界处尝试穿墙，会把边界也变成 `@` 符号。在边界处多次尝试穿墙，就获得了 flag1。

Flag2 需要通过游戏，不得不去看看代码了。先看到底为什么会导致穿墙：

~~~python

NewPos = list(CurPos)  # Line 393
FoundEnd = False
for NewDirection in NewDirections:
    ...                # NewPos[xxx] = yyy
    CurPos = NewPos    # Line 431
~~~

程序在每一步执行成功后，都会执行 `CurPos = NewPos`。但由于 `NewPos` 是个 `List`，后续对 `NewPos` 的更新会同步到 `CurPos` 中，是我们可以多做一步 invalid movement。并且这一步还不计入步数。

By the way，有了这层理解，让程序崩溃会更优雅一点。在第一关用合法的方向 + `u` 就可以崩溃了。

利用穿墙可以很容易通过前两关。第三关因为步数限制需要一定策略。

~~~python
#get a side opposite of where we start    Line 182
EndingSide = StartingSide ^ 1           # Line 183
~~~

从上面的注释可以知道，出口在入口的对侧方向。所以需要在向上的同时，尽可能的向对侧走。如果在早期遇到传送，可以利用传送将自己送到对侧。差不多手玩 4-5 次就通关了。



