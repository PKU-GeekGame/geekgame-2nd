一年一度的 GeekGame 结束了，Binary 分类的题又是一个不会。总分 1143，排名 82 ~~甚至比赛结束前两分钟还喜提排名-1~~，摆了.jpg

# 签到

下载文件，直接丢到 Chrome 浏览器打开，是可以正常复制的。直接粘贴到记事本里面，然后就可以看到 flag 了。

# 编原译理习题课

## 玩挺大

要在限时三秒内输出一个挺大的编译产物，Google 搜索 `compiler bomb` 相关的内容，随便找一个改一改.jpg
比如： `const int a[2147483]={195};int main(){};`

## 玩挺长

输出一个很长的报错，可以让引用层数变得很深，然后 g++ 就会一直输出 `#include nested too deeply` 的报错。

```cpp
#include __FILE__
#include __FILE__
#include __FILE__
#include __FILE__
#include __FILE__
int main(){}
```

# Flag Checker

简单的 Java 逆向题，直接丢到 jadx 里看反编译出的源码。

## Flag 1

源码里有一个 rot13 函数，判断部分将输入先 base64 再 rot13，因为 rot13 加解密算法一致，所以直接把函数揪出来编译运行即得flag

## Flag 2

这里用了一个叫做 nashorn 的 ScriptEngine。下面有一个 StringBuilder 用来构建传入的代码，同样也是揪出来运行，得到一串混淆了的 JavaScript 源码。肉眼反混淆一下就能写出解密代码

``` js
function checkflag2(_0xa83ex2){var _0x724b=['charCodeAt','map','','split','stringify','Correct','Wrong','j-'];return (JSON[_0x724b[4]](_0xa83ex2[_0x724b[3]](_0x724b[2])[_0x724b[1]](function(_0xa83ex3){return _0xa83ex3[_0x724b[0]](0)}))== JSON[_0x724b[4]]([0,15,16,17,30,105,16,31,16,67,3,33,5,60,4,106,6,41,0,1,67,3,16,4,6,33,232][_0x724b[1]](function(_0xa83ex3){return (checkflag2+ _0x724b[2])[_0x724b[0]](_0xa83ex3)}))?_0x724b[5]:_0x724b[6])}

function getFlag() {
    var _0x724b = ['charCodeAt', 'map', '', 'split', 'stringify', 'Correct', 'Wrong', 'j-'];
    return [0, 15, 16, 17, 30, 105, 16, 31, 16, 67, 3, 33, 5, 60, 4, 106, 6, 41, 0, 1, 67, 3, 16, 4, 6, 33, 232].map(function(f) {
        return (checkflag2 + _0x724b[2]).charCodeAt(f)
    }).map(function(f) {
        return String.fromCharCode(f)
    }).join('')
}
```
丢到浏览器里运行即可。

# 给钱不要

看了提示也只会做第二问，太菜了

在给出的[提示](https://chromium.googlesource.com/chromium/src/+/refs/tags/106.0.5249.163/components/omnibox/browser/autocomplete_input.cc#235)中，对于 JavaScript Bookmarklet 进行了一个正则匹配 `(?i)javascript:([^;=().\"]*)`，观察发现反斜杠和单引号并不在匹配列表中，这就很巧了，可以用 unicode 编码来构建一个能绕过正则的 payload。xssbot 会返回标题，所以 `document.title = document.body.innerHTML;`，unicode 编码后如下：

``` js
javascript:setTimeout `\u0064\u006f\u0063\u0075\u006d\u0065\u006e\u0074\u002e\u0074\u0069\u0074\u006c\u0065\u0020\u003d\u0020\u0064\u006f\u0063\u0075\u006d\u0065\u006e\u0074\u002e\u0062\u006f\u0064\u0079\u002e\u0069\u006e\u006e\u0065\u0072\u0048\u0054\u004d\u004c\u003b`//
```

结尾的 `//` 是为了注释掉js加上来的 `.jpg`。

# 这也能卷

## Flag1

进入题目后点击 Premium 然后发现被 debugger 卡掉了，再一看是高度混淆过的 js 搞的鬼，这条路基本上不能走了 ~~会变得不幸~~。

回到主页，看到 `main.js` 对 Premium 的判定 `localStorage.getItem('i_am_premium_user') === 'true'` 是完全在前端进行的，手动 setItem，再进入 Premium 页面，发现多了个 flag。

# 扫雷 II

## Flag 1

Golang的随机数，种子一致，随机数也一致。题目程序中的随机数是根据当前时间戳设置的，所以写个程序简单爆破一下。

``` golang
package main

import (
	"fmt"
	"math/rand"
	"time"
)

type Board = [16]int

func genBoard1() (board Board) {
	for i := 0; i < 16; i++ {
		for j := 0; j < 16; j++ {
			board[i] ^= ((rand.Intn(257)) % 2) << j
		}
	}
	return
}

func nearCount(board Board, x int, y int) int {
	if (board[x]>>y)&1 > 0 {
		return -1
	}
	delta := [8][2]int{{1, 0}, {-1, 0}, {0, 1}, {0, -1}, {1, 1}, {1, -1}, {-1, 1}, {-1, -1}}
	count := 0
	for _, d := range delta {
		tx, ty := x+d[0], y+d[1]
		if 0 <= tx && tx < 16 && 0 <= ty && ty < 16 {
			count += (board[tx] >> ty) & 1
		}
	}
	return count
}

func showBoard(board Board, marks Board) (result [16][16]int) {
	for i := 0; i < 16; i++ {
		for j := 0; j < 16; j++ {
			if (marks[i]>>j)&1 == 0 {
				result[i][j] = -2
			} else {
				result[i][j] = nearCount(board, i, j)
			}
		}
	}
	return
}

func main() {
	fullMarks := [16]int{0xffff, 0xffff, 0xffff, 0xffff, 0xffff, 0xffff, 0xffff, 0xffff, 0xffff, 0xffff, 0xffff, 0xffff, 0xffff, 0xffff, 0xffff, 0xffff}
	finalResult := // 这里塞输了一局之后的结果
	for i := -50000; i < 50000; i++ {
		loc, _ := time.LoadLocation("Asia/Shanghai")
		t1, _ := time.ParseInLocation("2006-01-02 15:04:05", "2022-11-19 21:49:54", loc)
		t := t1.UnixMilli()
		rand.Seed(t + int64(i))
		board := genBoard1()
		marks := fullMarks
		thisRound := showBoard(board, marks)
		for i := 0; i < 16; i++ {
			for j := 0; j < 16; j++ {
				if thisRound[i][j] != finalResult[i][j] {
					goto next
				}
			}
		}
		fmt.Println("seed:", t)
		board = genBoard1()
		fmt.Println(showBoard(board, marks))
		break
	next:
		continue
	}
}

```

可以得到下一局的布局，然后手动扫一下就好了 ~~（点错了好几次）~~


# 总结

这次 GeekGame：
- 科技并带着趣味
- 不觉得这很酷吗
- 作为一名理工男
- 我觉得这太酷了
- 很符合我对未来生活的想象

我太菜了.jpg