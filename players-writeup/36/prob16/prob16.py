flag = input("Flag: ").encode()
if len(set(flag)-set(range(127))) > 0:
    print("Wrong")
else:
    num = int.from_bytes(
        flag, "big") ^ 2511413510823273577350468206724207602459660000906919269554
    print(int.from_bytes(flag, "big"))
    print(num)
    print(hex(num)[2:])
    num_len = len(hex(num))-2
    print(num_len)
    for i in range(1, num_len+1):
        print(i, num >> ((num_len-i)*4))
        if (num >> ((num_len-i)*4)) % i > 0:
            print("Wrong")
            exit()
    print("Correct")
