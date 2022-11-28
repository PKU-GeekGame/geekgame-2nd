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

const baseUrl = "https://prob14-txffo964.geekgame.pku.edu.cn"
// const baseUrl = "http://localhost:8080"

type BoomReply struct {
	Board [16][16]int `json:"boom"`
}

type MyRand struct {
	List   []uint64
	Cursor int
}

var myRand MyRand

func (r *MyRand) Uint64() uint64 {
	r.Cursor = r.Cursor + 1
	for len(r.List) < r.Cursor {
		r.List = append(r.List, rand.Uint64())
	}
	return r.List[r.Cursor-1]
}

func (r *MyRand) Intn(n int) int {
	max := int64((1 << 63) - 1 - (1<<63)%uint64(n))
	v := int64(r.Uint64() & ((1 << 63) - 1))
	for v > max {
		v = int64(r.Uint64() & ((1 << 63) - 1))
	}
	return int(v % int64(n))
}

var secureVal byte

func genBoard1() (board Board) {
	for i := 0; i < 16; i++ {
		for j := 0; j < 16; j++ {
			board[i] ^= ((myRand.Intn(257)) % 2) << j
		}
	}
	return
}

func genBoard2() (board Board) {
	for i := 0; i < 4; i++ {
		dataBits := myRand.Uint64()
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
			board[i] ^= ((myRand.Intn(257)) % 2) << j
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
	myRand.Cursor = 0
	rn := int(myRand.Uint64()%20221119) + int(secureVal)
	myRand.Cursor = rn + 1
	curBoard := genBoard2()
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
	resp, err := http.PostForm(
		baseUrl+"/reset",
		url.Values{},
	)
	if err != nil {
		return err
	}
	body, _ := io.ReadAll(resp.Body)
	s := string(body)
	if !strings.Contains(s, "ok") {
		fmt.Println("Failed to get ok")
	}
	startTime := time.Now().UnixMilli()
	_, err = http.PostForm(
		baseUrl+"/init",
		url.Values{"level": {"2"}})
	if err != nil {
		return err
	}
	// make a boom and get board
	boomTips := BoomReply{}
	flag := false
	for i := 0; i < 16; i++ {
		for j := 0; j < 16; j++ {
			resp, _ := http.PostForm(
				baseUrl+"/click",
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
	for l := -100; l < 200; l++ {
		rand.Seed(startTime - int64(l))
		fmt.Println(startTime - int64(l))
		myRand.Cursor = 0
		myRand.List = nil
		_, err := http.Get(baseUrl + "/board")
		if err != nil {
			return err
		}
		for sec := 0; sec < 256; sec++ {
			secureVal = byte(sec)
			if checkSeed(boomTips) {
				fmt.Println("seed found", l, sec)
				return nil
			}
		}
	}
	fmt.Println("not found")
	return nil
}

func main() {
	err := getSeed()
	if err != nil {
		fmt.Println("error")
		return
	}
	board := genBoard2()
	showBoard(board)
	for i := 0; i < 16; i++ {
		for j := 0; j < 16; j++ {
			if nearCnt(board, i, j) != -1 {
				rep, _ := http.PostForm(
					baseUrl+"/click",
					url.Values{"x": {strconv.Itoa(i)}, "y": {strconv.Itoa(j)}})
				body, _ := io.ReadAll(rep.Body)
				s := string(body)
				if strings.Contains(s, "flag") {
					fmt.Println(s)
				}
			}
		}
	}
}
