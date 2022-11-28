package main
import (
	//securerand "crypto/rand"
	//"github.com/gin-gonic/gin"
	"math/rand"
	//"net/http"
	"os"
	//"strconv"
	"log"
	"fmt"
	"net/http"
	"net/url"
	"encoding/json"
	"io/ioutil"
	"strconv"
	"strings"
	"time"
)

type Board = [16]int
var UU string

func init() {
	file := "./" +"myans"+ ".txt"
	logFile, err := os.OpenFile(file, os.O_RDWR|os.O_CREATE|os.O_APPEND, 0766)
	if err != nil {
			panic(err)
	}
	log.SetOutput(logFile) // 将文件设置为log输出的文件
	// log.SetPrefix("[qSkipTool]")
	log.SetFlags(0)
	return
}

func genBoard3() (board Board) {
	for i := 1; i < 15; i++ {
		//secureVal := make([]byte, 2)
		//securerand.Read(secureVal)
		if i%2 == 0 {
			board[i] = 0x5554 //0xaaab
		} else {
			board[i] = 0x2aaa //0xd555
		}
	}
	for i := 0; i < 16; i++ {
		for j := 0; j < 16; j++ {
			board[i] ^= ((rand.Intn(257)) % 2) << j
		}
	}
	//log.Println("genBoard3",board)
	//PrintBoard(board)
	return
}

func PrintBoard(board Board) [16][16] int{
	var result [16][16] int

	for i := 0; i < 16; i++ {
		if i%2 ==0 {
			for j := 0; j < 16; j++ {
				if (0x5554>>j)&1==0{
					result[i][j]=(board[i]>>j)&1
				}else{
					result[i][j]=-1
				}		
			}
		}else{
			for j := 0; j < 16; j++ {
				if (0x2aaa>>j)&1==0{
					result[i][j]=(board[i]>>j)&1
				}else{
					result[i][j]=-1
				}		
			}
		}
	}
	for i := 0; i < 16; i++{
		log.Println(result[i])
	}
	return result
}

func main() {
	UU="http://127.0.0.1:8080"
	UU="https://prob14-pslk2tan.geekgame.pku.edu.cn"
	fmt.Println(("begin"))
	var ram [16*10000*60]int //储存随机数
	var array [16][16]int
	//n:=len(ram)
	counter:=0 //当前储存随机数个数
	var board Board
	var t int64 //随机种子
	t=time.Now().UnixMilli()-2000
	//t=1669212646530-10
	log.Println(t)
	//reset
	http.PostForm(UU+"/reset", url.Values{
		"level":  {strconv.Itoa(2)},
	})
	
	//选择level
	http.PostForm(UU+"/init", url.Values{
		"level":  {strconv.Itoa(3)},
	})


	for offset:=0; offset < 20000; offset++{
		//种子加偏移
		log.Println(t+int64(offset))
		rand.Seed(t+int64(offset))

		genBoard := genBoard3
		//验证这个种子是否符合以前的棋盘
		flag:=1
		for j := 0; j < counter; j++ {
			if j%16==0{
				board=genBoard()
			}
			if j%2==0{
				if (board[j%16]&0xaaab)!=(ram[j]&0xaaab){
					flag=0
					break
				}
			} else {
				if (board[j%16]&0xd555)!=(ram[j]&0xd555){
					flag=0
					break
				}
			}	
		}
		log.Println(flag)
		if flag==1 && counter==0{
			//测试当前棋盘
			board=genBoard()
			get_boom:=0
			for tx := 0; tx < 16; tx++ {
				for ty := 0; ty < 16; ty++ {
					is_boom:=(board[tx] >> ty) & 1
					if is_boom==0{
						strbody:=Postclick(tx,ty)
						if strings.Contains(strbody,"flag"){
							fmt.Println(strbody)
							fmt.Println(offset)
							os.Exit(3)
						}else if !strings.Contains(strbody,"ok"){
							array=JsonToMap(strbody)["boom"]
							//log.Println(array)
							get_boom=1
							break
						}
					}
				}
				if get_boom==1{
					break
				}
			}
			if get_boom==1{
				//遇到炸弹，记录随机数
				for i := 0; i < 16; i++ {
					num:=0
					for j := 0; j < 16; j++ {
						if array[i][j]==-1{
							num|=1<<j
						}
					}
					//log.Println(num)
					ram[counter]=num
					counter++
				}
			}
			//log.Println(ram[:counter])
		} else if flag==1 && counter!=0{
			//找到随机种子
			log.Println("found!")
			board=genBoard()
			res:=PrintBoard((board))
			//扫掉能确定的块
			for i := 0; i < 16; i++ {
				for j := 0; j < 16; j++ {
					if res[i][j]==0{
						strbody:=Postclick(i,j)
						if !strings.Contains(strbody,"ok"){
							log.Println("ERROR!!!")
							os.Exit(3)
						}
					}
				}
			}

			//阻塞
			fmt.Scanln()
			os.Exit(3)
		}
	}
	
	return
}

func JsonToMap(str string) map[string] [16][16] int {
 
	var tempMap map[string] [16][16] int
 
	err := json.Unmarshal([]byte(str), &tempMap)
 
	if err != nil {
		panic(err)
	}
 
	return tempMap
}

func Postclick(x int,y int) string{
	
	res, err := http.PostForm(UU+"/click", url.Values{
		"x":  {strconv.Itoa(x)},
		"y":  {strconv.Itoa(y)},
	})
	if err != nil {
		log.Println(err.Error())
		os.Exit(3)
	}

	defer res.Body.Close()

	body,err := ioutil.ReadAll(res.Body)
	if err != nil {
		log.Println(err.Error())
		os.Exit(3)
	}

	strbody:=string(body)
	log.Println(strbody)

	return strbody
}