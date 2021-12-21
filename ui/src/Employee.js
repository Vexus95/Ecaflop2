export default class Employee {
  static fields = [
    'name',
    'email',
    'address_line1',
    'address_line2',
    'city',
    'zip_code'
  ]

  static initialData () {
    const res = {}
    for (const field of Employee.fields) {
      res[field] = ''
    }
    return res
  }

  static getPayloadFromElement (element) {
    const payload = {}
    for (const field of Employee.fields) {
      payload[field] = element[field]
    }
    return payload
  }
}
