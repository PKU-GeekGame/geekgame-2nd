# 我用108天录了个音

## 录音

采用 [TTS 语音合成](https://www.narakeet.com/languages/chinese-text-to-speech-zh/#trynow) 生成了原始音频文件。

## 调整间隔

采用 Adobe Audition 加入静音。通过本地测试微调静音时长。得到文件 [tts.mp3](./tts.mp3)。

## 修改时长

一开始想手动修改文件元数据但没有成功。经过若干尝试之后，发现用 Audition 将 `.mp3` 另存为 `.aac` 后，`ffprobe` 会计算出错误时长。生成的 [tts.aac](./tts.aac) 文件识别成功率不高，但多试了几次之后还是顺利拿到了 Flag 1（`flag{4G + HemonyOS > 5G}`）。

## 减小文件体积

上一步成功的文件体积很大（超过了 700 K），想要拿到 Flag 2 得要尝试新的方法。

没做出来。
