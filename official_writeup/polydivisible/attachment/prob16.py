flag=input("Flag: ").encode()
if len(set(flag)-set(range(127)))>0:
    print("Wrong")
else:
    num=int.from_bytes(flag,"big")^2511413510787461238669866766355566039743902103765988701586
    num_len=len(hex(num))-2
    for i in range(1,num_len+1):
        if (num>>((num_len-i)*4))%i>0:
            print("Wrong")
            exit()
    print("Correct")