package main

import (
	securerand "crypto/rand"
	"encoding/json"
	"fmt"
	"io"
	"math/rand"
	"net/http"
	"net/url"
	"strconv"
	"strings"
	"time"
)

type Board = [16]int

const baseUrl = "https://prob14-jilihmym.geekgame.pku.edu.cn"

type BoomReply struct {
	Board [16][16]int `json:"boom"`
}

func genBoard1() (board Board) {
	for i := 0; i < 16; i++ {
		for j := 0; j < 16; j++ {
			board[i] ^= ((rand.Intn(257)) % 2) << j
		}
	}
	return
}

func genBoard2() (board Board) {
	for i := 0; i < 4; i++ {
		dataBits := rand.Uint64()
		for j := 0; j < 4; j++ {
			board[4*i+j] = int(dataBits>>(16*j)) & 0xffff
		}
	}
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
	return
}

func nearCnt(board Board, x int, y int) int {
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

func showBoard(board Board) {
	for i := 0; i < 16; i++ {
		for j := 0; j < 16; j++ {
			fmt.Print((board[i] >> j) & 1)
		}
		fmt.Println()
	}
	return
}

func checkSeed(reply BoomReply) bool {
	curBoard := genBoard1()
	for i := 0; i < 16; i++ {
		for j := 0; j < 16; j++ {
			// fmt.Print(nearCnt(curBoard, i, j), " ")
			if nearCnt(curBoard, i, j) != reply.Board[i][j] {
				return false
			}
		}
	}
	return true

}

func getSeed() error {
	// set seed
	_, err := http.PostForm(
		baseUrl + "/reset",
		url.Values{},
	)
	if err != nil {
		return err
	}
	_, err = http.PostForm(
		baseUrl + "/init",
		url.Values{"level": {"1"}})
	if err != nil {
		return err
	}
	// make a boom and get board
	boomTips := BoomReply{}
	flag := false
	for i := 0; i < 16; i++ {
		for j := 0; j < 16; j++ {
			resp, _ := http.PostForm(
				baseUrl + "/click",
				url.Values{"x": {strconv.Itoa(i)}, "y": {strconv.Itoa(j)}})
			body, _ := io.ReadAll(resp.Body)
			s := string(body)
			if strings.Contains(s, "boom") {
				err := json.Unmarshal(body, &boomTips)
				if err != nil {
					return err
				}
				flag = true
				break
			}
		}
		if flag {
			break
		}
	}
	// try possible seeds
	startTime := time.Now().UnixMilli()
	for l := -300; l < 600; l++ {
		rand.Seed(startTime - int64(l))
		if checkSeed(boomTips) {
			fmt.Println("seed found",l)
			return nil
		}
	}
	fmt.Println("not found")
	return nil
}

func main() {
	getSeed()
	board := genBoard1()
	showBoard(board)
	for i := 0; i < 15; i++ {
		for j := 0; j < 16; j++ {
			if nearCnt(board,i,j) != -1 {
				http.PostForm(
					baseUrl + "/click",
					url.Values{"x": {strconv.Itoa(i)}, "y": {strconv.Itoa(j)}})
			}
		}
	}
}
