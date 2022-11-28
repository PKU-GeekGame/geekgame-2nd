package main

import (
	"fmt"
	"strconv"
	// securerand "crypto/rand"
	"math/rand"
	"net/http"
	"net/url"
	"encoding/json"
	"log"
	"io"
	"time"
)

type Board = [16]int

var tmprands []uint64
var tmprand_pointer int

func randUint64() uint64 {
	if len(tmprands) == tmprand_pointer {
		tmprands = append(tmprands, rand.Uint64())
	}
	tmprand_pointer++
	return tmprands[tmprand_pointer - 1]
}

func randInt63() int64 {
	return int64(randUint64() & ((1 << 63) - 1))
}

func randInt63n(n int64) int64 {
	// return int(randInt63n(int64(n)))
	if n&(n-1) == 0 {
		return randInt63() & (n - 1)
	}
	max := int64((1 << 63) - 1 - (1<<63)%uint64(n))
	v := randInt63()
	for v > max {
		v = randInt63()
	}
	return v % n
}

func randInt31() int32 {
	return int32(randInt63() >> 32)
}

func randInt31n(n int32) int32 {
	if n <= 0 {
		panic("invalid argument to Int31n")
	}
	if n&(n-1) == 0 { // n is power of two, can mask
		return randInt31() & (n - 1)
	}
	max := int32((1 << 31) - 1 - (1<<31)%uint32(n))
	v := randInt31()
	for v > max {
		v = randInt31()
	}
	return v % n
}

func randIntn(n int) int {
	if n <= 0 {
		panic("invalid argument to Intn")
	}
	if n <= 1<<31-1 {
		return int(randInt31n(int32(n)))
	}
	return int(randInt63n(int64(n)))
}

func clearRandStorage() {
	tmprand_pointer = 0
	tmprands = nil
}

func clearRandStoragePreserve() {
	tmprands = tmprands[tmprand_pointer:]
	tmprand_pointer = 0
}

func restoreRand() {
	tmprand_pointer = 0
}

func genBoard1() (board Board) {
	for i := 0; i < 16; i++ {
		for j := 0; j < 16; j++ {
			board[i] ^= ((randIntn(257)) % 2) << j
		}
	}
	return
}

func genBoard2() (board Board) {
	for i := 0; i < 4; i++ {
		dataBits := randUint64()
		// fmt.Println("test genBoard2 ", dataBits)
		for j := 0; j < 4; j++ {
			board[4*i+j] = int(dataBits>>(16*j)) & 0xffff
		}
	}
	return
}

var board3Mask Board

func genBoard3Mask() {
	for i := 1; i < 15; i++ {
		// secureVal := make([]byte, 2)
		// securerand.Read(secureVal)
		// if i%2 == 0 {
		// 	board[i] = (int(secureVal[0])*256 + int(secureVal[1])) & 0x5554
		// } else {
		// 	board[i] = (int(secureVal[0])*256 + int(secureVal[1])) & 0x2aaa
		// }
		if i % 2 == 0 {
			board3Mask[i] = 0x5554
		} else {
			board3Mask[i] = 0x2aaa
		}
	}
}

func genBoard3() (board Board) {
	for i := 0; i < 16; i++ {
		for j := 0; j < 16; j++ {
			board[i] ^= ((randIntn(257)) % 2) << j
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

func getJson(rbody io.ReadCloser, target interface{}) error {
	defer rbody.Close()

	return json.NewDecoder(rbody).Decode(target)
}

type InitResponse struct {
	Ok string `json:"ok"`
	Error string `json:"error"`
}

func serverInit(mineServer string, level int) {
	resp, err := http.PostForm(
		fmt.Sprintf("%s/init", mineServer),
		url.Values{
			"level": {strconv.Itoa(level)},
		},
	)
	if err != nil {
		log.Fatal(err)
	}
	
	var res InitResponse
	json.NewDecoder(resp.Body).Decode(&res)
	// fmt.Printf("%+v\n", res)
	if res.Error != "" || res.Ok != "OK" {
		log.Fatal(res)
	}
}

func serverReset(mineServer string) {
	resp, err := http.PostForm(
		fmt.Sprintf("%s/reset", mineServer),
		url.Values{
		},
	)
	if err != nil {
		log.Fatal(err)
	}
	
	var res InitResponse
	json.NewDecoder(resp.Body).Decode(&res)
	// fmt.Printf("%+v\n", res)
	if res.Error != "" || res.Ok != "" {
		log.Fatal(res)
	}
}

type ClickResponse struct {
	Ok *int `json:"ok"`
	Error *string `json:"error"`
	Boom *[16][16]int `json:"boom"`
	Flag *string `json:"flag"`
}

func serverClick(mineServer string, x int, y int) ClickResponse {
	resp, err := http.PostForm(
		fmt.Sprintf("%s/click", mineServer),
		url.Values{
			"x": {strconv.Itoa(x)},
			"y": {strconv.Itoa(y)},
		},
	)
	if err != nil {
		log.Fatal(err)
	}
	
	var res ClickResponse
	json.NewDecoder(resp.Body).Decode(&res)
	// fmt.Printf("%+v\n", res)
	if res.Error != nil {
		log.Fatal(res)
	}
	if res.Boom != nil {
		fmt.Println("server BOOM at ", x, y)
	}
	return res
}

func tryServer(mineServer string, marks Board) (lastBoard Board) {
	for x := 0; x < 16; x++ {
		for y := 0; y < 16; y++ {
			if (marks[x] >> y & 1) > 0 {
				continue  // skip booms
			}
			clickRet := serverClick(mineServer, x, y)
			if clickRet.Boom != nil {
				for i := 0; i < 16; i++ {
					rowI := 0
					for j := 0; j < 16; j++ {
						if clickRet.Boom[i][j] == -1 {
							rowI |= 1 << j;
						}
					}
					lastBoard[i] = rowI
				}
				return
			} else if clickRet.Flag != nil {
				fmt.Println("SUCCESS: FLAG = ", *clickRet.Flag)
				lastBoard = marks
				return
			}
		}
	}
	log.Fatal("tryServer failed")
	return
}

func main() {
	mineServer := "https://prob14-ebvgvlmq.geekgame.pku.edu.cn"
	// fullMarks := [16]int{0xffff, 0xffff, 0xffff, 0xffff, 0xffff, 0xffff, 0xffff, 0xffff, 0xffff, 0xffff, 0xffff, 0xffff, 0xffff, 0xffff, 0xffff, 0xffff}
	zeroMarks := [16]int{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0}

	serverReset(mineServer)
	seedRandStart := time.Now().UnixMilli() + 700

	// // get our first boom.
	// serverInit(mineServer, 1)
	// lastBoard := tryServer(mineServer, zeroMarks) // BOOM here.
	// fmt.Println("first board:", lastBoard)

	// var curBoard Board
	
	// // reverse find first seed
	// for seedRand := seedRandStart; ; seedRand-- {
	// 	rand.Seed(seedRand)
	// 	clearRandStorage()
	// 	curBoard = genBoard1()
	// 	if curBoard == lastBoard {
	// 		fmt.Println("FOUND first SEED:", seedRand)
	// 		fmt.Println("Difference:", seedRandStart - seedRand)
	// 		break
	// 	}
	// }

	// // exploit to find first flag
	// curBoard = genBoard1()
	// tryServer(mineServer, curBoard)

	// // now we try the second flag,
	// // which needs some trial and error.
	// serverInit(mineServer, 2)
	// lastBoard := tryServer(mineServer, zeroMarks) // BOOM here.
	// fmt.Println("first board:", lastBoard)

	// // reverse find first seed
	// for seedRand := seedRandStart; ; seedRand-- {
	// 	rand.Seed(seedRand)
	// 	clearRandStorage()
		
	// 	rn_base := int(randUint64() % 20221119)
	// 	for i := 0; i < rn_base; i += 1 {
	// 		randUint64()
	// 	}
	// 	clearRandStoragePreserve()

	// 	var valBoard Board
	// 	for secureVal := 0; secureVal < 256; secureVal++ {
	// 		restoreRand()
	// 		for i := 0; i < secureVal; i += 1 {
	// 			randUint64()
	// 		}
	// 		valBoard = genBoard2()
	// 		if valBoard == lastBoard {
	// 			fmt.Println("The actual round is ", secureVal)
	// 			break
	// 		}
	// 	}
	// 	if valBoard == lastBoard {
	// 		fmt.Println("FOUND second SEED:", seedRand)
	// 		break
	// 	}
	// }
	
	// // exploit to find second flag
	// curBoard := genBoard2()
	// tryServer(mineServer, curBoard)

	genBoard3Mask()
	serverInit(mineServer, 3)
	lastBoard := tryServer(mineServer, zeroMarks) // BOOM here.
	fmt.Println("first board:", lastBoard)

	var curBoard Board
	
	// reverse find first seed
	for seedRand := seedRandStart; ; seedRand-- {
		rand.Seed(seedRand)
		clearRandStorage()
		curBoard = genBoard3()
		if curBoard[0] == lastBoard[0] {
			fmt.Println("FOUND first SEED:", seedRand)
			fmt.Println("Difference:", seedRandStart - seedRand)
			break
		}
	}
	nextBoard := genBoard3()

	// auto solver..
	var ourBoard [16][16]int
	for i := 0; i < 16; i++ {
		for j := 0; j < 16; j++ {
			if (board3Mask[i] >> j & 1) > 0 {
				ourBoard[i][j] = -2
				continue
			}
			if (nextBoard[i] >> j & 1) > 0 {
				ourBoard[i][j] = -1
				fmt.Println("markflag(", i, ",", j, ");")
			} else {
				fmt.Println("clickbutton(", i, ",", j, ");")
				ourBoard[i][j] = *serverClick(mineServer, i, j).Ok
			}
		}
	}

	for {
		updated := false
		for x := 0; x < 16; x++ {
			for y := 0; y < 16; y++ {
				if ourBoard[x][y] < 0 {
					continue
				}
				delta := [8][2]int{{1, 0}, {-1, 0}, {0, 1}, {0, -1}, {1, 1}, {1, -1}, {-1, 1}, {-1, -1}}
				possible_count := 0
				boom_count := 0
				for _, d := range delta {
					tx, ty := x+d[0], y+d[1]
					if 0 <= tx && tx < 16 && 0 <= ty && ty < 16 {
						if ourBoard[tx][ty] < 0 {
							possible_count++
						}
						if ourBoard[tx][ty] == -1 {
							boom_count++
						}
					}
				}
				if possible_count == ourBoard[x][y] {
					// mark all as booms
					for _, d := range delta {
						tx, ty := x+d[0], y+d[1]
						if 0 <= tx && tx < 16 && 0 <= ty && ty < 16 {
							if ourBoard[tx][ty] == -2 {
								updated = true
								ourBoard[tx][ty] = -1
								fmt.Println("markflag(", tx, ",", ty, ");")
							}
						}
					}
				} else if boom_count == ourBoard[x][y] {
					// mark all as non-booms
					for _, d := range delta {
						tx, ty := x+d[0], y+d[1]
						if 0 <= tx && tx < 16 && 0 <= ty && ty < 16 {
							if ourBoard[tx][ty] == -2 {
								fmt.Println("clickbutton(", tx, ",", ty, ");")
								ourBoard[tx][ty] = *serverClick(mineServer, tx, ty).Ok
							}
						}
					}
				}
			}
		}
		if !updated {
			break
		}
	}
}
