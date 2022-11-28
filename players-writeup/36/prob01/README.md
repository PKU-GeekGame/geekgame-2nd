# 小北问答 · 极速版

> 题目顺序随机，与下面的次序可能不同。

## WebP 支持

支持 WebP 图片格式的最早 Firefox 版本是多少？
答案格式：^\d+$

在 [Can I Use](https://caniuse.com/?search=webp) 上可以查询到答案为 `65`。

## 猜质数

我刚刚在脑海中想了一个介于 9967888929 到 9967889236 之间的质数。猜猜它是多少？
答案格式：^\d+$

区间范围是随机生成的，保证中间一共有 8 个质数，所以需要随机猜一个。

## 电子游戏概论

在第一届 PKU GeekGame 比赛的题目《电子游戏概论》中，通过第 11 级关卡需要多少金钱？
答案格式：^\d+$

关卡数字是随机的。

在 `geekgame-1st` 仓库中的 `src/pygame/game/server/libtreasure.py` 中找到下面这一行

```py
GOAL_OF_LEVEL = lambda level: 300+int(level**1.5)*100
```

## Host 请求头

访问网址 “http://ctf.世界一流大学.com” 时，向该主机发送的 HTTP 请求中 Host 请求头的值是什么？
答案格式：^[^:\s]+$

使用 Insomnia 或者 Postman 发送请求，查看请求头即可得到答案 `ctf.xn--4gqwbu44czhc7w9a66k.com`

## AV <-> BV

视频 bilibili.com/video/BV1EV411s7vu 也可以通过 bilibili.com/video/av_____ 访问。下划线内应填什么数字？
答案格式：^\d+$

使用 [av-bv 转换器](https://ivanlulyf.github.io/bilibili-av-bv-converter/) 即可得到答案 `418645518`。

## gStore

北京大学某实验室曾开发了一个叫 gStore 的数据库软件。最早描述该软件的论文的 DOI 编号是多少？
答案格式：^[\d.]+\/[\d.]+$

在 Google Scholar 上检索到对应的论文 [gStore: answering SPARQL queries via subgraph matching](https://dl.acm.org/doi/abs/10.14778/2002974.2002976?casa_token=ewohkNyvuN0AAAAA:0NwOI7DJS2mthcRmwj5rObi3PyFSYvpa_AnZnMlDwzmxpyZQW6vVx6l0AtuDME2gt-KwCUZfp-_yKUc) 即可得到答案 `10.14778/2002974.2002976`。

## PKU Runner

每个 Android 软件都有唯一的包名。北京大学课外锻炼使用的最新版 PKU Runner 软件的包名是什么？
答案格式：^[a-z.]+$

下载 [APK](https://github.com/pku-runner/pku-runner.github.io/releases/download/v1.2.4/pkurunner-v1.2.4.apk) 后使用 [apktool](https://ibotpeaches.github.io/Apktool/install/) 解析：

```sh
apktool d pkurunner-v1.2.4.apk
```

在解码后得到的 `pkurunner-v1.2.4/AndroidManifest.xml` 中找到 `package` 属性即可得到答案 `cn.edu.pku.pkurunner`。

## MAC 地址到邮政编码（坑题）

我有一个朋友在美国，他无线路由器的 MAC 地址是 d2:94:35:21:42:43。请问他所在地的邮编是多少？
答案格式：^\d+$

本题无解。

## 速通

速通需要写脚本，见 [interact.py](./interact.py)。因为质数要猜，而 MAC 这道题无解，所以通过概率只有 1/64。因为有 Rate limit，所以加上 sleep 慢慢等即可。
