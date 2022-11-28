package main

import (
	securerand "crypto/rand"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"math/rand"
	"net/http"
	"net/url"
	"time"
)

type Board = [16]int

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

func genBoard3_1() (board Board) {
	for i := 0; i < 16; i++ {
		for j := 0; j < 16; j++ {
			board[i] ^= ((rand.Intn(257)) % 2) << j
		}
	}
	return
}

const HOST = "https://prob14-rnbuvqwm.geekgame.pku.edu.cn"

func parse(resp *http.Response) map[string]interface{} {
	respBody, _ := ioutil.ReadAll(resp.Body)
	respBytes := []byte(string(respBody))
	var respJson map[string]interface{}
	_ = json.Unmarshal(respBytes, &respJson)
	return respJson
}

func main() {
	t := time.Now().UnixMilli()
	resp, _ := http.Post(HOST+"/reset", "application/json", nil)
	resp, _ = http.PostForm(HOST+"/init", url.Values{"level": {"3"}})

	for j := 0; j < 16; j++ {
		resp, _ = http.PostForm(HOST+"/click",
			url.Values{"x": {"0"}, "y": {fmt.Sprintf("%d", j)}})
		respJson := parse(resp)

		if val, ok := respJson["boom"]; ok {
			arr, _ := val.([]interface{})
			board := Board{}
			for i := 0; i < 16; i++ {
				row, _ := arr[i].([]interface{})
				for j := 0; j < 16; j++ {
					if row[j].(float64) < 0 {
						board[i] |= 1 << j
					}
				}
			}

			for guess := t - 1000; guess <= t+1000; guess++ {
				fmt.Println("Guess: ", guess)
				rand.Seed(guess)
				myBoard := genBoard3()
				if myBoard[0] == board[0] && myBoard[15] == board[15] {
					fmt.Print("The server is reset at ")
					fmt.Println(time.UnixMilli(guess))

					nextBoard := genBoard3_1()
					for i := 0; i < 16; i++ {
						for j := 0; j < 16; j++ {
							if i == 0 || i == 15 || (i%2 == 0 && ((1<<j)&0x5554) == 0) || (i%2 == 1 && ((1<<j)&0x2aaa) == 0) {
								if (nextBoard[i]>>j)&1 == 0 {
									resp, _ = http.PostForm(HOST+"/click",
										url.Values{"x": {fmt.Sprintf("%d", i)}, "y": {fmt.Sprintf("%d", j)}})
									respJson = parse(resp)
									if val, ok := respJson["ok"]; ok {
										nei := int(val.(float64))
										fmt.Print(nei)
									}
								} else {
									fmt.Print("X")
								}
							} else {
								fmt.Print("*")
							}
						}
						fmt.Println()
					}

					fmt.Println("It is your turn now...")
					return
				}
			}

			fmt.Println("Failed to solve!")
			return
		}
	}
}
