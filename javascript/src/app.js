const Koa = require('koa')
const koaBody = require('koa-body')
const Router = require('@koa/router')
const Repository = require('./repository')

const app = new Koa()
const router = new Router()

router.get('/', (ctx, next) => {
  ctx.type = 'text/html'
  ctx.body = 'This is the index'
  next()
})

router.get('/employee/:id', async (ctx, next) => {
  const { id } = ctx.params
  const result = await ctx.repository.getEmployeedById(id)
  ctx.body = result
  next()
})

router.post('/employee/new', async (ctx, next) => {
  const { name, email } = ctx.request.body
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

app.use(koaBody({ jsonLimit: '1kb' })).use(router.routes()).use(router.allowedMethods())

module.exports = app

const main = async () => {
  const repository = new Repository('hr.db')
  await repository.init()
  app.context.repository = repository
  app.listen(3000)
}

if (!module.parent) {
  main()
}
