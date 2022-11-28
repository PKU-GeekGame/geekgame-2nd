package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"math/rand"
	"net/http"
	"net/url"
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

const HOST = "https://prob14-5dl2hxr2.geekgame.pku.edu.cn"

func parse(resp *http.Response) map[string]interface{} {
	respBody, _ := ioutil.ReadAll(resp.Body)
	respBytes := []byte(string(respBody))
	var respJson map[string]interface{}
	_ = json.Unmarshal(respBytes, &respJson)
	return respJson
}

func main() {
	var flag1 string

	t := time.Now().UnixMilli()
	resp, _ := http.Post(HOST+"/reset", "application/json", nil)
	resp, _ = http.PostForm(HOST+"/init", url.Values{"level": {"1"}})

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

			for guess := t; guess <= t+10000; guess++ {
				rand.Seed(guess)
				if genBoard1() == board {
					fmt.Print("The server is reset at ")
					fmt.Println(time.UnixMilli(guess))

					nextBoard := genBoard1()
					fmt.Println("You are going to succeed, just wait for a while...")
					for i := 0; i < 16; i++ {
						for j := 0; j < 16; j++ {
							if (nextBoard[i]>>j)&1 == 1 {
								fmt.Print("*")
							} else {
								resp, _ = http.PostForm(HOST+"/click",
									url.Values{"x": {fmt.Sprintf("%d", i)}, "y": {fmt.Sprintf("%d", j)}})
								respJson = parse(resp)

								if val, ok := respJson["ok"]; ok {
									nei := int(val.(float64))
									fmt.Print(nei)
								}

								if val, ok := respJson["flag"]; ok {
									flag1 = val.(string)
								}
							}
						}
						fmt.Println()
					}
					fmt.Println("Flag 1: " + flag1)
					return
				}
			}
		}
	}
}
