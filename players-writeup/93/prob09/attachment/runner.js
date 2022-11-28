Object.entries(Object.getOwnPropertyDescriptors(Math))
  .map((e) => e[0])
  .filter((e) => typeof e === 'string')
  .forEach((key) => (globalThis[key] = Math[key]))

const arg = process.argv.find((str) => str.startsWith('-e='))
if (!arg) process.exit(1)
const expression = Buffer.from(arg.slice(3), 'base64').toString()
Promise.resolve(eval(expression)).then((result) =>
  console.log(JSON.stringify(result))
)
