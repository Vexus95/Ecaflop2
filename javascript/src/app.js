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
  ctx.body = employees
  next()
})

router.delete('/api/v1/employees', async (ctx, next) => {
  const deleted = await ctx.repository.deleteEmployees()
  ctx.body = { deleted }
  next()
})

router.get('/api/v1/employee/:id', async (ctx, next) => {
  const { id } = ctx.params
  const employee = await ctx.repository.getEmployeedById(id)
  ctx.body = { employee }
  next()
})

router.put('/api/v1/employee/:id', async (ctx, next) => {
  const { id } = ctx.params
  const { name, email, address_line1, address_line2, city, zip_code } = ctx.request.body
  await ctx.repository.updateEmployee(id, { name, email, address_line1, address_line2, city, zip_code })
  ctx.body = { status: 'updated' }
  next()
})

router.put('/api/v1/employee', async (ctx, next) => {
  const { name, email, address_line1, address_line2, city, zip_code } = ctx.request.body
  if (!name) {
    ctx.throw(400, 'name is required')
  }
  if (!email) {
    ctx.throw(400, 'email is required')
  }
  if (!address_line1) {
    ctx.throw(400, 'address_line1 is required')
  }
  if (!address_line2) {
    ctx.throw(400, 'address_line2 is required')
  }
  if (!city) {
    ctx.throw(400, 'city is required')
  }
  if (!zip_code) {
    ctx.throw(400, 'zip_code is required')
  }
  const id = await ctx.repository.insertEmployee({ name, email, address_line1, address_line2, city, zip_code })
  ctx.status = 201
  ctx.body = { employee: { id, name, email } }
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
