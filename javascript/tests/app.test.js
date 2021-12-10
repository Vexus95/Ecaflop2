const Repository = require('../src/repository')
const app = require('../src/app')
const assert = require('chai').assert
const server = app.listen()
const request = require('supertest').agent(server)

const textContains = (expected) => {
  return (response) => {
    assert.include(response.text, expected)
  }
}

describe('server', () => {
  before(async () => {
    const repository = new Repository(':memory:')
    await repository.init()
    app.context.repository = repository
  })

  after(() => {
    server.close()
  })

  specify('index route should show the index text', async () => {
    await request.get('/').expect(200).expect(textContains('index'))
  })

  specify('GET /employee/<id> works', async () => {
    const id = await app.context.repository.insertEmployee({ name: 'John', email: 'john@corp.tld' })
    const response = await request.get(`/employee/${id}`).expect(200)
    const body = response.body
    assert.deepEqual(body, { name: 'John', email: 'john@corp.tld', id })
  })

  specify('POST /employee/new', async () => {
    const response = await request.post('/employee/new').type('form').send({ name: 'Alice', email: 'alice@corp.tld' }).expect(201)
    assert.isOk(response.body.id)
  })
})
