/* eslint-disable camelcase */
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
              email TEXT NOT NULL,
              address_line1 TEXT NOT NULL,
              address_line2 TEXT NOT NULL,
              city TEXT NOT NULL,
              zip_code TEXT NOT NULL
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

  async insertEmployee ({ name, email, address_line1, address_line2, city, zip_code }) {
    const statement = await this.db.prepare(
        `
        INSERT INTO employee
          (name, email, address_line1, address_line2, city, zip_code)
        VALUES
            (?, ?, ?, ?, ?, ?)
         `
    )
    await statement.run([name, email, address_line1, address_line2, city, zip_code])
    const response = await this.db.get('SELECT last_insert_rowid() AS id')
    return response.id
  }

  async getEmployeeById (id) {
    const response = await this.db.get(`
        SELECT
          id, name, email, address_line1, address_line2, city, zip_code
        FROM
          employee
        WHERE
        id = ?
        `,
    id
    )
    return response
  }

  async getEmployees (id) {
    const response = await this.db.all(`
      SELECT
          id, name, email, address_line1, address_line2, city, zip_code
      FROM
        employee
        `
    )
    return response
  }

  async deleteEmployee (id) {
    const statement = await this.db.prepare(`DELETE FROM employee WHERE id = ?`)
    await statement.run([id])
  }

  async updateEmployee (id, fields) {
    const { name, email, address_line1, address_line2, city, zip_code } = fields
    const statement = await this.db.prepare(`
       UPDATE employee
       SET
         name=?, email=?, address_line1=?, address_line2=?, city=?, zip_code=?
       WHERE
         id=?
     `)
    await statement.run([name, email, address_line1, address_line2, city, zip_code, id])
  }

  async deleteEmployees () {
    const result = await this.db.run('DELETE FROM employee')
    return result.changes
  }
}

module.exports = Repository
