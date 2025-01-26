import { open, Database } from 'sqlite'
import sqlite3 from 'sqlite3'
import { afterAll, beforeAll, expect, test } from '@jest/globals'
import axios from 'axios'

const DATABASE_PATH = '../backend/db.sqlite3'
let db: Database

beforeAll(async () => {
  db = await open({filename: DATABASE_PATH, driver : sqlite3.Database })
})

afterAll(async () => {
  await db.close()
})

test('adding a team', async () => {
  const url = 'http://127.0.0.1:8000/add_team'
  const params = new URLSearchParams()
  params.append('name', 'Typescript devs')
  await axios.post(url, params)

  const res = await db.all('SELECT name FROM hr_team')

  expect(res).toEqual([{name: 'Typescript devs' }])
})
