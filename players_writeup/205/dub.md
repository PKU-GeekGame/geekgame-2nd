# 我用108天录了个音

## 解题过程
只解出 flag1，压制相关的内容搜起来太杂了，，，找不到关键。

看了提示得知可以用 ogg 文件存储多段录音，从而让 ffprobe 不能准确得到时长。

先用 `ffmpeg` 转换文件的格式，采样率，声道数。

~~~python
import os
for i in range(5):
    os.system(f'ffmpeg -i {i}.m4a -ac 1 -ar 8000 {i}.ogg')
~~~

生成 silence：
~~~bash
ffmpeg -f lavfi -i anullsrc=r=11025:cl=mono -t 9 -acodec aac out.m4a
ffmpeg -i out.m4a -ac 1 -ar 8000 silence.ogg
~~~

然后 wiki 到 ogg 文件的格式：

> The format consists of chunks of data each called an "Ogg page".
> 
> Bitstreams may also be appended to existing files, a process known as "chaining", to cause the bitstreams to be decoded in sequence.

所以只需要把文件按顺序拼接就行了。

~~~python
def merge():
    voices = [f'{i}.ogg' for i in range(4)]
    voices = ' silence.ogg '.join(voices)
    os.system(f'cat {voices} > test.ogg')
~~~
