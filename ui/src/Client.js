export default class Client {
  constructor (path) {
    this.url = 'http://127.0.0.1:5678/api/v1' + path
  }

  onRequestStart (element) {
    element.loading = true
    element.error = ''
  }

  onRequestSuccess (element) {
    element.loading = false
    element.error = ''
    element.success = true
  }

  onRequestError (element, error) {
    element.loading = false
    element.error = error
  }

  async update (element, name, fields) {
    this.onRequestStart(element)
    try {
      const data = { }
      for (const field of fields) {
        data[field] = element[field]
      }
      const response = await fetch(this.url, {
        method: 'put',
        body: JSON.stringify(data)
      })
      if (!response.ok) {
        throw new Error(`Request failed with status ${response.status}`)
      }
      const json = await response.json()
      element.status = json.status
      this.onRequestSuccess(element)
    } catch (error) {
      this.onRequestError(element, error)
    }
  }

  async fetch (element, name, fields) {
    this.onRequestStart(element)
    try {
      const response = await fetch(this.url)
      if (!response.ok) {
        throw new Error(`Request failed with status ${response.status}`)
      }
      const json = await response.json()
      const newValues = json[name]
      for (const field of fields) {
        const newValue = newValues[field]
        element[field] = newValue
      }
      this.onRequestSuccess(element)
    } catch (error) {
      this.onRequestError(element, error)
    }
  }
}
