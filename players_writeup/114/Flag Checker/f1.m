x='MzkuM8gmZJ6jZJHgnaMuqy4lMKM4';
resb64 = rrot(x)
res = matlab.net.base64decode(resb64);
res = char(res)

function x=rrot(x)
    i1=(x>='n'&x<='z');
    i2=(x>='a'&x<='m');
    i3=(x>='N'&x<='Z');
    i4=(x>='A'&x<='M');
    i5=(x>='0'&x<='4');
    i6=(x>='5'&x<='9');
    x(i1)=x(i1)-13;
    x(i2)=x(i2)+13;
    x(i3)=x(i3)-13;
    x(i4)=x(i4)+13;
    x(i5)=x(i5)+5;
    x(i6)=x(i6)-5;
end