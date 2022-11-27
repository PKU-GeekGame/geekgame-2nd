// @ts-check
import fastify from 'fastify'
import fastifyStatic from '@fastify/static'
import { join } from 'path'
import { runInNodeSandbox, runInBrowserSandbox } from './sandbox.js'
import { ROOT_DIR } from './misc.js'

const server = fastify()

server.post(
  '/submit',
  {
    schema: {
      body: {
        type: 'object',
        properties: {
          expr: {
            type: 'string',
            pattern: '^([a-z0-9+\\-*/%(), ]|([0-9]+[.])+[0-9]+)+$'
          },
          mode: { type: 'string', enum: ['node', 'browser'] }
        },
        required: ['expr', 'mode']
      }
    }
  },
  async (req) => {
    // @ts-ignore
    const { expr, mode } = req.body
    const result = await (mode === 'node'
      ? runInNodeSandbox(expr)
      : runInBrowserSandbox(expr))
    return { result }
  }
)

server.register(fastifyStatic, {
  root: join(ROOT_DIR, '..', 'frontend')
})

console.log(await server.listen({ port: 3000, host: '0.0.0.0' }))
