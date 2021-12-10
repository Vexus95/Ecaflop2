const sqlite3 = require('sqlite3')
const open = require('sqlite').open
const fs = require('fs')

class Repository {
  constructor (dbPath) {
    this.dbPath = dbPath
    this.db = null
    this.shouldMigrate = !fs.existsSync(this.dbPath)
  }

  async migrate () {
    await this.db.exec(`
            CREATE TABLE employee(
              id INTEGER PRIMARY KEY,
              name TEXT NOT NULL,
              email TEXT NOT NULL
             )
         `)
  }

  async init () {
    this.db = await open({
      filename: this.dbPath,
      driver: sqlite3.Database
    })
    if (this.shouldMigrate) {
      await this.migrate()
    }
  }

  async insertEmployee ({ name, email }) {
    const statement = await this.db.prepare('INSERT INTO employee(name, email) VALUES (?, ?)')
    await statement.run([name, email])
    const response = await this.db.get('SELECT last_insert_rowid() AS id')
    return response.id
  }

  async getEmployeedById (id) {
    const response = await this.db.get('SELECT name, email, id FROM employee WHERE id = ?', id)
    return response
  }
}

module.exports = Repository
