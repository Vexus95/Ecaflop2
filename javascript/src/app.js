const Koa = require('koa')
const koaBody = require('koa-body')
const cors = require('@koa/cors')
const logger = require('koa-logger')
const Router = require('@koa/router')

const Repository = require('./repository')

const app = new Koa()
const router = new Router()

router.get('/api/v1/employees', async (ctx, next) => {
  const employees = await ctx.repository.getEmployees()
  ctx.body = { employees }
  next()
})

router.delete('/api/v1/employees', async (ctx, next) => {
  const deleted = await ctx.repository.deleteEmployees()
  ctx.body = { deleted }
  next()
})

router.get('/api/v1/employee/:id', async (ctx, next) => {
  const { id } = ctx.params
  const result = await ctx.repository.getEmployeedById(id)
  ctx.body = result
  next()
})

router.put('/api/v1/employee/:id', async (ctx, next) => {
  const { id } = ctx.params
  const { name, email } = JSON.parse(ctx.request.body)
  const result = await ctx.repository.updateEmployee(id, { name, email })
  ctx.body = result
  next()
})

router.put('/api/v1/employee', async (ctx, next) => {
  console.log(ctx.request.body)
  const { name, email } = JSON.parse(ctx.request.body)
  if (!name) {
    ctx.throw(400, 'name is required')
  }
  if (!email) {
    ctx.throw(400, 'email is required')
  }
  const id = await ctx.repository.insertEmployee({ name, email })
  ctx.status = 201
  ctx.body = { id, name, email }
  next()
})

app
  .use(logger())
  .use(cors({ origin: ['http://127.0.0.1:8080'] }))
  .use(koaBody({ jsonLimit: '1kb' }))
  .use(router.routes())
  .use(router.allowedMethods())

module.exports = app

const main = async () => {
  const repository = new Repository('hr.db')
  await repository.init()
  app.context.repository = repository
  console.log('Listening on 0.0.0.0:5678')
  app.listen(5678)
}

if (!module.parent) {
  main()
}
