// @ts-check
import { launch } from 'puppeteer'
import { pathToFileURL } from 'url'
import { promisify } from 'util'
import { execFile } from 'child_process'
import { resolve } from 'path'
import { NODE_PATH, ROOT_DIR } from './misc.js'
const execFileAsync = promisify(execFile)
const sandboxUrl = pathToFileURL(resolve(ROOT_DIR, 'sandbox.html')).href

/**
 * @param {string} expr
 */
export async function runInNodeSandbox(expr) {
  const args = [
    '--experimental-policy=policy.json',
    '--policy-integrity=sha256-1NvUvTeQqHoo+XJv7zUAobD/VEaIGQ8CB3471GP2isY=',
    'runner.js',
    '-e=' + Buffer.from(expr).toString('base64')
  ]
  const result = await execFileAsync(NODE_PATH, args, {
    timeout: 10000,
    cwd: ROOT_DIR,
    shell: false
  })
  return JSON.parse(result.stdout)
}

/**
 * @param {string} expr
 */
export async function runInBrowserSandbox(expr) {
  const browser = await launch({
    executablePath: 'google-chrome-stable',
    args: ['--no-sandbox']
  })
  try {
    const page = await browser.newPage()
    await page.goto(sandboxUrl)
    const result = await page.evaluate(expr)
    await browser.close()
    return result
  } catch (err) {
    await browser.close()
    throw err
  }
}
