package main

import (
	// securerand "crypto/rand"
	// "github.com/gin-gonic/gin"
	"math/rand"
	// "os"
	"strconv"
	"time"
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
}

func main() {
	url_value := url.Values{}
	url_value.Add("level", "3")
	http.PostForm("https://prob14-xqahgn6k.geekgame.pku.edu.cn/init", url_value)
	var i = 0
	var j = 0
	var data board
	var msg message
	for {
		url_value = url.Values{}
		url_value.Add("x", strconv.Itoa(i))
		url_value.Add("y", strconv.Itoa(j))
		resp, _ := http.PostForm("https://prob14-xqahgn6k.geekgame.pku.edu.cn/click", url_value)
		body, _:= ioutil.ReadAll(resp.Body)
		if body[2] == 98 {
			json.Unmarshal(body, &data)
			break
		}
		j += 1
		if j == 16 {
			i += 1
			j = 0
		}
	}
	cur_t := time.Now().UnixMilli()
	var real_seed int64
	real_seed = 0
	for seed := cur_t - 10000; seed < cur_t; seed++ {
		rand.Seed(seed)
		flag := true
		for i := 0; i < 16; i++ {
			for j := 0; j < 16; j++ {
				x := rand.Intn(257) % 2
				if (i == 0 || i == 15) && x == 1 && data.Board[i][j] != -1 {
					flag = false
				}
				if (i == 0 && i == 15) && x == 0 && data.Board[i][j] == -1 {
					flag = false
				}
			}
		}
		if flag {
			real_seed = seed
			fmt.Println(real_seed)
		}
	}
	rand.Seed(real_seed)
	for i := 0; i < 16; i++ {
		for j := 0; j < 16; j++ {
			rand.Intn(257)
		}
	}
	for i := 0; i < 16; i++ {
		for j := 0; j < 16; j++ {
			x := 1 - rand.Intn(257)%2
			if i != 0 && i != 15 &&
				((i%2 == 0 && ((0x5554 >> j) & 1 == 1)) ||
					(i % 2 != 0 && ((0x2aaa >> j) & 1 == 1))) {
				x = -1
				fmt.Print("? ")
			} else {
				fmt.Print(x)
				fmt.Print(" ")
			}
			if x != 1 {
			 	continue
			}
			url_value = url.Values{}
			url_value.Add("x", strconv.Itoa(i))
			url_value.Add("y", strconv.Itoa(j))
			resp, _ := http.PostForm("https://prob14-xqahgn6k.geekgame.pku.edu.cn/click", url_value)
			body, _:= ioutil.ReadAll(resp.Body)
			json.Unmarshal(body, &msg)
		}
		fmt.Println("")
	}
}
