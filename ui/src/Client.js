export default class Client {
  constructor (element) {
    if (process.env.NODE_ENV === 'production') {
      this.baseUrl = process.env.VUE_APP_HR_API_URL
    } else {
      this.baseUrl = 'http://127.0.0.1:5678/api/v1'
    }
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
        const message = await this.getErrorMessage(response)
        throw new Error(message)
      }
      this.onRequestSuccess()
      const json = await response.json()
      return json
    } catch (error) {
      this.onRequestError(error)
    }
  }

  async getErrorMessage (response) {
    try {
      const json = await response.json()
      return json.error
    } catch (e) {
      return `Request failed with status ${response.status}`
    }
  }
}
