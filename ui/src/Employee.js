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

  static updateElementFromJson (element, json) {
    for (const field of Employee.fields) {
      element[field] = json[field]
    }
  }

  static updateBodyfromElement (element) {
    const body = {}
    for (const field of Employee.fields) {
      body[field] = element[field]
    }
    return body
  }
}
