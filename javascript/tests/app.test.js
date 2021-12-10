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
  after(() => {
    server.close()
  })

  specify('index route should show the index text', async () => {
    await request.get('/').expect(200).expect(textContains('index'))
  })
})
