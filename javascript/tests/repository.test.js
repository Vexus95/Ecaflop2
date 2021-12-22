const Repository = require('../src/repository')
const assert = require('chai').assert

describe('repository', () => {
  it('can be initialized', async () => {
    const repository = new Repository(':memory:')
    await repository.init()
  })

  it('can insert employees', async () => {
    const repository = new Repository(':memory:')
    await repository.init()
    await repository.insertEmployee({ name: 'John', email: 'john@corp.tld' })
  })

  it('can retrieve employees', async () => {
    const repository = new Repository(':memory:')
    await repository.init()
    const id = await repository.insertEmployee({ name: 'John', email: 'john@corp.tld' })

    const actual = await repository.getEmployeeById(id)

    assert.deepEqual(actual, { name: 'John', email: 'john@corp.tld', id })
  })
})
