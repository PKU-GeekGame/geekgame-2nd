// @ts-check
import { fileURLToPath } from 'url'
import { dirname } from 'path'
import { createRequire } from 'module'
const filename = fileURLToPath(import.meta.url)
export const ROOT_DIR = dirname(filename)
export const NODE_PATH = process.execPath
globalThis.require = createRequire(filename)
