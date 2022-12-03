const axios = require('axios')
const test = require('tape')
const sqlite3 = require('sqlite3')
const open = require('sqlite').open

test('adding a team', async (t) => {
  let url = 'http://127.0.0.1:8000/reset_db'
  await axios.post(url)

  url = 'http://127.0.0.1:8000/add_team'
  const params = new URLSearchParams()
  params.append('name', 'devs')
  const response = await axios.post(url, params)

  const db = await open({
    filename: '../../../backend/db.sqlite3',
    driver: sqlite3.Database
  })
  const res = await db.get('SELECT name FROM hr_team')
  t.deepEqual(res, { name: 'devs' })
  t.end()
})
