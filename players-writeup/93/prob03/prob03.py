import random

import pwn
import sympy
import re

GOAL_OF_LEVEL = lambda level: 300+int(level**1.5)*100
r = pwn.remote('prob03.geekgame.pku.edu.cn', 10003)
r.recvuntil(b'Please input your token:')
r.sendline(b'key')

counter=0
level=1


while 1:
    massge=r.recvuntil('(estart)\n'.encode('utf-8')).decode('utf-8')
    print(massge)

    if "Congratulations!" in massge:
        level=level+1
        counter=0

    #先算出迷宫部分
    maze=massge.split('\n')[:-1]
    while not "####" in maze[0]:
        maze=maze[1:]

    
    if level<3:
        if "E" in massge[:-15]:
            print("find E!")
            ans=input()
            print(ans)
            r.sendline(ans.encode('utf-8'))
            
            counter=counter+1
            print("steps",counter)
        else:  
            for i in range(len(maze)):
                j= maze[i].find('@')
                if j!=-1:
                    print("found!")
                    break
            
            if not maze[i-1][j] in "X#":
                ans="nu"
            elif not maze[i][j-1] in "X#":
                ans="wu"
            elif not maze[i][j+1] in "X#":
                ans="eu"
            elif not maze[i+1][j] in "X#":
                ans="su"
            else:
                ans=input()
                
            print(ans)
            r.sendline(ans.encode('utf-8'))

            counter=counter+1
            print("steps",counter)
    else:
        #向下一层看看E坐标
        if not maze[i-1][j] in "X#":
            ans="nd"
        elif not maze[i][j-1] in "X#":
            ans="wd"
        elif not maze[i][j+1] in "X#":
            ans="ed"
        elif not maze[i+1][j] in "X#":
            ans="sd"
        else:
            print("error in step3")
            ans=input()

        print(ans)
        r.sendline(ans.encode('utf-8'))

        counter=counter+1
        print("steps",counter)
        
        massge=r.recvuntil('(estart)\n'.encode('utf-8')).decode('utf-8')
        print(massge)
        #先算出迷宫部分
        maze=massge.split('\n')[:-1]
        while not "####" in maze[0]:
            maze=maze[1:]

        #保存E坐标
        for i in range(len(maze)):
            j= maze[i].find('E')
            if j!=-1:
                print("found E!")
                break
        iE=i
        jE=j

        #刷新
        ans="r"
        print(ans)
        r.sendline(ans.encode('utf-8'))

        counter=counter+1
        print("steps",counter)



        #边向上边靠近E
        while 1:
            massge=r.recvuntil('(estart)\n'.encode('utf-8')).decode('utf-8')
            print(massge)
            #先算出迷宫部分
            maze=massge.split('\n')[:-1]
            while not "####" in maze[0]:
                maze=maze[1:]

            if "E" in massge[:-15]:
                print("find E!")
                r.interactive()
                ans=input()
                print(ans)
                r.sendline(ans.encode('utf-8'))
                
                counter=counter+1
                print("steps",counter)
                r.interactive()
            else:
                for i in range(len(maze)):
                    j= maze[i].find('@')
                    if j!=-1:
                        print("found!")
                        break
                
                if i>iE and not maze[i-1][j] in "X#":
                    ans="nu"
                elif j>jE and not maze[i][j-1] in "X#":
                    ans="wu"
                elif j<jE and not maze[i][j+1] in "X#":
                    ans="eu"
                elif i<iE and not maze[i+1][j] in "X#":
                    ans="su"
                elif not maze[i-1][j] in "X#":
                    ans="nu"
                elif not maze[i][j-1] in "X#":
                    ans="wu"
                elif not maze[i][j+1] in "X#":
                    ans="eu"
                elif not maze[i+1][j] in "X#":
                    ans="su"
                else:
                    ans=input()
                print(i,j)
                print(iE,jE)
                print(ans)
                r.sendline(ans.encode('utf-8'))

                counter=counter+1
                print("steps",counter)

        counter=counter+1
        print("steps",counter)

        

        