package main

import (
	// securerand "crypto/rand"
	// "github.com/gin-gonic/gin"
	// "os"
	"strconv"
	"io/ioutil"
	"encoding/json"
	"net/http"
	"net/url"
	"fmt"
)

type board struct {
	Board [16][16]int `json:"boom"`
}

type message struct {
	Ok int `json:"ok"`
	Flag string `json:"flag"`
	Board [16][16]int `json:"boom"`
}

const (
	rngLen   = 607
	rngTap   = 273
	rngMax   = 1 << 63
	rngMask  = rngMax - 1
	int32max = (1 << 31) - 1
)

var (
	tap int
	feed int
	vec [rngLen]int64
)

func Uint64() uint64 {
	tap--
	if tap < 0 {
		tap += rngLen
	}

	feed--
	if feed < 0 {
		feed += rngLen
	}

	x := vec[feed] + vec[tap]
	vec[feed] = x
	return uint64(x)
}

func main() {
	url_value := url.Values{}
	url_value.Add("level", "2")
	http.PostForm("https://prob14-ecf8a94t.geekgame.pku.edu.cn/init", url_value)
	var i = 0
	var j = 0
	tap = 1
	feed = rngLen - rngTap + 1
	var msg message
	for num := 1; num <= 152; num ++ {
		for {
			var data board
			var test_data [16]int
			url_value = url.Values{}
			url_value.Add("x", strconv.Itoa(i))
			url_value.Add("y", strconv.Itoa(j))
			resp, _ := http.PostForm("https://prob14-ecf8a94t.geekgame.pku.edu.cn/click", url_value)
			body, _:= ioutil.ReadAll(resp.Body)
			if body[2] == 98 {
				json.Unmarshal(body, &data)
				for cnt := 0; cnt < 4; cnt ++ {
					var res int64
					res = 0
					for x := cnt * 4; x < (cnt + 1) * 4; x++ {
						for y := 0; y < 16; y++ {
							var t int64
							if data.Board[x][y] == -1 {
								t = 1
							}
							if data.Board[x][y] != -1 {
								t = 0
							}
							// fmt.Print("asdasd ")
							// fmt.Println(t)
							res |= t << ((x - cnt*4) * 16 + y)
							// fmt.Print("asdasdasd ")
							// fmt.Println(t << ((i - cnt*4) * 16 + j))
						}
					}
					for y := 0; y < 4; y++ {
						test_data[4*cnt+y] = int(res>>(16*y)) & 0xffff
					}
					tap--
					if tap < 0 {
						tap += rngLen
					}

					feed--
					if feed < 0 {
						feed += rngLen
					}
					vec[feed] = res
					if num <= 20 {
						fmt.Println(res)
					}
				}
				// fmt.Println(data.Board[1])
				// for x := 0; x < 16; x++ {
				// 	fmt.Print((test_data[1]>>x)&1)
				// 	fmt.Print(" ")
				// }
				// fmt.Println("")
				// fmt.Println("======================")
				// fmt.Println(data.Board)
				for x := 0; x < 16; x++ {
					for y := 0; y < 16; y++ {
						if ((test_data[x]>>y) & 1 > 0) && data.Board[x][y] != -1 {
							fmt.Println("GG!")
						}
						if (((test_data[x]>>y)) & 1 == 0) && data.Board[x][y] == -1 {
							fmt.Println("GG!")
						}
					}
				}
				break
			}
			j += 1
			if j == 16 {
				i += 1
				j = 0
			}
		}
	}
	var board [16]int
	fmt.Println(vec)
	for i := 0; i < 4; i++ {
		dataBits := Uint64()
		for j := 0; j < 4; j++ {
			board[4*i+j] = int(dataBits>>(16*j)) & 0xffff
		}
	}
	for i := 0; i < 16; i++ {
		for j := 0; j < 16; j++ {
			if (board[i]>>j)&1 > 0 {
				continue
			}
			url_value = url.Values{}
			url_value.Add("x", strconv.Itoa(i))
			url_value.Add("y", strconv.Itoa(j))
			resp, _ := http.PostForm("https://prob14-ecf8a94t.geekgame.pku.edu.cn/click", url_value)
			body, _:= ioutil.ReadAll(resp.Body)
			json.Unmarshal(body, &msg)
			fmt.Println(msg)
		}
	}
}
