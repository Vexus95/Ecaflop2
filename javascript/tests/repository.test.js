const Repository = require('../src/repository')
const assert = require('chai').assert

const JOHN = {
  name: 'John',
  email: 'john@corp.tld',
  address_line1: 'line 1',
  address_line2: 'line 2',
  city: 'paris',
  zip_code: '75001'
}

describe('repository', () => {
  it('can be initialized', async () => {
    const repository = new Repository(':memory:')
    await repository.init()
  })

  it('can insert employees', async () => {
    const repository = new Repository(':memory:')
    await repository.init()
    const id = await repository.insertEmployee(JOHN)
    assert.isAtLeast(1, id)
  })

  it('can retrieve employees', async () => {
    const repository = new Repository(':memory:')
    await repository.init()
    const id = await repository.insertEmployee(
      {
        name: 'John',
        email: 'john@corp.tld',
        address_line1: 'line 1',
        address_line2: 'line 2',
        city: 'paris',
        zip_code: '75001'
      })

    const actual = await repository.getEmployeeById(id)
    const expected = { id, ...JOHN }
    assert.deepEqual(actual, expected)
  })
})
