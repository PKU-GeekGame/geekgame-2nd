# 企鹅文档

## 解题过程
因为之前不清楚 Chrome 可以直接搜 network 包的内容，所以解法可能比较蠢，，，

在 Chrome developing tools 的 Source Panel 下会看到一个 opendoc 的文件，对应的 network 请求为 `https://docs.qq.com/dop-api/opendoc?...&startrow=0&endrow=60...` (略去了部分 query params 以防信息泄露)。

在里面可以发现文档中的部分内容，并且隐藏的内容也是有的，但是不全，只有 60 行。然后发现链接里有 `endrow=60`，将其改成 70 再 fetch 一次，即可获得完整链接过第一关。

第二关一开始找不到流量，自己上传了一个类似的文档，然后也调到修订记录的界面。点击记录会重新加载页面。这时 Chrome 记录到 4 个流量包，挨个下载下来进行搜索，就可以确认文档的内容在哪个包里。

然后将下载的 .har 文件拖到 Chrome 的 Network Panel 里，搜索同样的文件 `sheet?u=`。然后就可以获得 flag 文档的信息。其中标黑的部分对用有内容的编号，按一行 11 个进行输出即可。







