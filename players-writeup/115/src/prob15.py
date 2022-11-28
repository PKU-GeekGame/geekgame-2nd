import base64
def rot13(s):
    sb=""
    for i in range(len(s)):
        charAt = s[i]
        if (charAt >= 'a' and charAt <= 'm'):
            charAt = chr(ord(charAt) + ord('\r'))
        elif (charAt >= 'A' and charAt <= 'M'):
            charAt = chr(ord(charAt) + ord('\r'))
        elif (charAt >= 'n' and charAt <= 'z'):
            charAt=chr(ord(charAt) - ord('\r'))
        elif (charAt >= 'N' and charAt <= 'Z'):
            charAt=chr(ord(charAt) - ord('\r'))
        elif (charAt >= '5' and charAt <= '9'):
            charAt = chr(ord(charAt) - 5)
        elif (charAt >= '0' and charAt <= '4'):
            charAt = chr(ord(charAt) + 5)
        sb+=charAt
    return sb

flag1=base64.b64decode(rot13("MzkuM8gmZJ6jZJHgnaMuqy4lMKM4"))
print(flag1)
# flag{s1mp1e-jvav_rev}

ss = '\u0089\u009a\u0081\u008c\u009b\u0086\u0080\u0081Ï\u008c\u0087\u008a\u008c\u0084\u0089\u0083\u008e\u0088ÝÇ°ß\u0097\u008e×Ü\u008a\u0097ÝÆ\u0094\u0099\u008e\u009dÏ°ß\u0097ØÝÛ\u008dÒ´È\u008c\u0087\u008e\u009d¬\u0080\u008b\u008a®\u009bÈÃÈ\u0082\u008e\u009fÈÃÈÈÃÈ\u009c\u009f\u0083\u0086\u009bÈÃÈ\u009c\u009b\u009d\u0086\u0081\u0088\u0086\u0089\u0096ÈÃÈ¬\u0080\u009d\u009d\u008a\u008c\u009bÈÃÈ¸\u009d\u0080\u0081\u0088ÈÃÈ\u0085ÂÈ²Ô\u009d\u008a\u009b\u009a\u009d\u0081ÏÇ¥¼ ¡´°ß\u0097ØÝÛ\u008d´Û²²Ç°ß\u0097\u008e×Ü\u008a\u0097Ý´°ß\u0097ØÝÛ\u008d´Ü²²Ç°ß\u0097ØÝÛ\u008d´Ý²Æ´°ß\u0097ØÝÛ\u008d´Þ²²Ç\u0089\u009a\u0081\u008c\u009b\u0086\u0080\u0081Ç°ß\u0097\u008e×Ü\u008a\u0097ÜÆ\u0094\u009d\u008a\u009b\u009a\u009d\u0081Ï°ß\u0097\u008e×Ü\u008a\u0097Ü´°ß\u0097ØÝÛ\u008d´ß²²ÇßÆ\u0092ÆÆÒÒÏ¥¼ ¡´°ß\u0097ØÝÛ\u008d´Û²²Ç´ßÃÞÚÃÞÙÃÞØÃÜßÃÞßÚÃÞÙÃÜÞÃÞÙÃÙØÃÜÃÜÜÃÚÃÙßÃÛÃÞßÙÃÙÃÛÞÃßÃÞÃÙØÃÜÃÞÙÃÛÃÙÃÜÜÃÝÜÝ²´°ß\u0097ØÝÛ\u008d´Þ²²Ç\u0089\u009a\u0081\u008c\u009b\u0086\u0080\u0081Ç°ß\u0097\u008e×Ü\u008a\u0097ÜÆ\u0094\u009d\u008a\u009b\u009a\u009d\u0081ÏÇ\u008c\u0087\u008a\u008c\u0084\u0089\u0083\u008e\u0088ÝÄÏ°ß\u0097ØÝÛ\u008d´Ý²Æ´°ß\u0097ØÝÛ\u008d´ß²²Ç°ß\u0097\u008e×Ü\u008a\u0097ÜÆ\u0092ÆÆÐ°ß\u0097ØÝÛ\u008d´Ú²Õ°ß\u0097ØÝÛ\u008d´Ù²Æ\u0092'
u=""
for i in ss:
    u+=chr(ord(i)^ 0xEF)
print(u)
# function checkflag2(_0xa83ex2){var _0x724b=['charCodeAt','map','','split','stringify','Correct','Wrong','j-'];return (JSON[_0x724b[4]](_0xa83ex2[_0x724b[3]](_0x724b[2])[_0x724b[1]](function(_0xa83ex3){return _0xa83ex3[_0x724b[0]](0)}))== JSON[_0x724b[4]]([0,15,16,17,30,105,16,31,16,67,3,33,5,60,4,106,6,41,0,1,67,3,16,4,6,33,232][_0x724b[1]](function(_0xa83ex3){return (checkflag2+ _0x724b[2])[_0x724b[0]](_0xa83ex3)}))?_0x724b[5]:_0x724b[6])}

"""
function checkflag2(a) {
    var b = ['charCodeAt', 'map', '', 'split', 'stringify', 'Correct', 'Wrong', 'j-']
    return (JSON['stringify'](a['split']('')['map'](function(c) {
        return c['charCodeAt'](0)
    })) == JSON['stringify']([0, 15, 16, 17, 30, 105, 16, 31, 16, 67, 3, 33, 5, 60, 4, 106, 6, 41, 0, 1, 67, 3, 16, 4, 6, 33, 232]['map'](function(c) {
        return (checkflag2 + '')['charCodeAt'](c)
    })) ? 'Correct': 'Wrong')
}
"""

# 浏览器执行：JSON['stringify']([0, 15, 16, 17, 30, 105, 16, 31, 16, 67, 3, 33, 5, 60, 4, 106, 6, 41, 0, 1, 67, 3, 16, 4, 6, 33, 232]['map'](function(c) {return (checkflag2 + '')['charCodeAt'](c)}))
r = [102, 108, 97, 103, 123, 106, 97, 118, 97, 115, 99, 114, 105, 112, 116, 45, 111, 98, 102, 117, 115, 99, 97, 116, 111, 114, 125]
flag2=""
for i in r:
    flag2+=chr(i)
print(flag2)
# flag{javascript-obfuscator}