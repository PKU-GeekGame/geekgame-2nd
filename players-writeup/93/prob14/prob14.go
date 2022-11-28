package main

import (
	securerand "crypto/rand"
	"github.com/gin-gonic/gin"
	"math/rand"
	"net/http"
	"os"
	"strconv"
	"time"
	"log"
)

type Board = [16]int

func init() {
	file := "./" +"message"+ ".txt"
	logFile, err := os.OpenFile(file, os.O_RDWR|os.O_CREATE|os.O_APPEND, 0766)
	if err != nil {
			panic(err)
	}
	log.SetOutput(logFile) // 将文件设置为log输出的文件
	// log.SetPrefix("[qSkipTool]")
	log.SetFlags(0)
	return
}

func genBoard1() (board Board) {
	for i := 0; i < 16; i++ {
		for j := 0; j < 16; j++ {
			board[i] ^= ((rand.Intn(257)) % 2) << j
		}
	}
	log.Println("genBoard1",board)
	return
}

func genBoard2() (board Board) {
	for i := 0; i < 4; i++ {
		dataBits := rand.Uint64()
		for j := 0; j < 4; j++ {
			board[4*i+j] = int(dataBits>>(16*j)) & 0xffff
		}
	}
	log.Println("genBoard2",board)
	return
}

func genBoard3() (board Board) {
	for i := 1; i < 15; i++ {
		secureVal := make([]byte, 2)
		securerand.Read(secureVal)
		if i%2 == 0 {
			board[i] = (int(secureVal[0])*256 + int(secureVal[1])) & 0x5554
		} else {
			board[i] = (int(secureVal[0])*256 + int(secureVal[1])) & 0x2aaa
		}
	}
	for i := 0; i < 16; i++ {
		for j := 0; j < 16; j++ {
			board[i] ^= ((rand.Intn(257)) % 2) << j
		}
	}
	log.Println("genBoard3",board)
	return
}

func checkWin(board Board, marks Board) bool {
	for i := 0; i < 16; i++ {
		if board[i]|marks[i] != 0xffff {
			return false
		}
	}
	return true
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
	//rand.Seed(time.Now().UnixMilli())
	t:=time.Now().UnixMilli()
	rand.Seed(t)
	log.Println("set seed",t)
	flagFiles := [4]string{"", "flag1", "flag2", "flag3"}
	level := 0
	r := gin.Default()
	var genBoard func() Board
	var curBoard Board
	var curMarks Board
	fullMarks := [16]int{0xffff, 0xffff, 0xffff, 0xffff, 0xffff, 0xffff, 0xffff, 0xffff, 0xffff, 0xffff, 0xffff, 0xffff, 0xffff, 0xffff, 0xffff, 0xffff}
	r.LoadHTMLFiles("index.html")
	r.POST("/init", func(c *gin.Context) {
		if level > 0 {
			c.JSON(http.StatusOK, gin.H{
				"error": "Game already initialized",
			})
		} else {
			lv := c.PostForm("level")
			if lv == "1" {
				level = 1
				genBoard = genBoard1
				curBoard = genBoard()
				c.JSON(http.StatusOK, gin.H{
					"ok": "OK",
				})
			} else if lv == "2" {
				level = 2
				secureVal := make([]byte, 1)
				securerand.Read(secureVal)
				rn := int(rand.Uint64()%20221119) + int(secureVal[0])
				log.Println("secureVal",int(secureVal[0]))
				log.Println("rn",int(rn))
				for i := 0; i < rn; i += 1 {
					rand.Uint64()
				}
				genBoard = genBoard2
				curBoard = genBoard()
				c.JSON(http.StatusOK, gin.H{
					"ok": "OK",
				})
			} else if lv == "3" {
				level = 3
				genBoard = genBoard3
				curBoard = genBoard()
				c.JSON(http.StatusOK, gin.H{
					"ok": "OK",
				})
			} else {
				c.JSON(http.StatusOK, gin.H{
					"error": "Invalid level",
				})
			}
		}

	})
	r.POST("/click", func(c *gin.Context) {
		if level == 0 {
			c.JSON(http.StatusOK, gin.H{
				"error": "Not initialized",
			})
		} else {
			x_ := c.PostForm("x")
			y_ := c.PostForm("y")

			//log.Println(x_)
			//log.Println(y_)

			x, err1 := strconv.Atoi(x_)
			y, err2 := strconv.Atoi(y_)
			if err1 != nil || err2 != nil || x < 0 || x >= 16 || y < 0 || y >= 16 {
				c.JSON(http.StatusOK, gin.H{
					"error": "Invalid input",
				})
			} else {
				nearCnt := nearCount(curBoard, x, y)
				if nearCnt == -1 {
					respose := gin.H{
						"boom": showBoard(curBoard, fullMarks),
					}
					curBoard = genBoard()
					curMarks = [16]int{}
					c.JSON(http.StatusOK, respose)
				} else {
					curMarks[x] |= (1 << y)
					if checkWin(curBoard, curMarks) {
						curBoard = genBoard()
						curMarks = [16]int{}
						dat, _ := os.ReadFile(flagFiles[level])
						c.JSON(http.StatusOK, gin.H{
							"ok":   nearCnt,
							"flag": string(dat),
						})
					} else {
						c.JSON(http.StatusOK, gin.H{
							"ok": nearCnt,
						})
					}
				}
			}
		}
	})
	r.POST("/reset", func(c *gin.Context) {
		level = 0
		t:=time.Now().UnixMilli()
		rand.Seed(t)
		log.Println("reset seed",t)
		c.JSON(http.StatusOK, gin.H{
			"ok": "",
		})
	})
	r.GET("/board", func(c *gin.Context) {
		if level == 0 {
			c.JSON(http.StatusOK, gin.H{
				"error": "Not initialized",
			})
		} else {
			c.JSON(http.StatusOK, gin.H{
				"board": showBoard(curBoard, curMarks),
			})
		}
	})
	r.GET("/", func(c *gin.Context) {
		c.HTML(http.StatusOK, "index.html", nil)
	})
	r.Run(":8080")
}
