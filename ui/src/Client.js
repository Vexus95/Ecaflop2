export default class Client {
  constructor (element) {
    this.baseUrl = 'http://127.0.0.1:5678/api/v1'
    this.element = element
  }

  onRequestStart () {
    this.element.loading = true
    this.element.error = ''
  }

  onRequestSuccess () {
    this.element.loading = false
    this.element.error = ''
    this.element.success = true
  }

  onRequestError (error) {
    this.element.loading = false
    this.element.error = error
  }

  async doRequest (path, options) {
    const url = this.baseUrl + path
    const headers = new Headers()
    headers.append('Content-Type', 'application/json')
    const fetchOptions = { headers, ...options }
    this.onRequestStart()
    try {
      const response = await fetch(url, fetchOptions)
      if (!response.ok) {
        throw new Error(`Request failed with status ${response.status}`)
      }
      this.onRequestSuccess()
      const json = await response.json()
      return json
    } catch (error) {
      this.onRequestError(error)
    }
  }
}
