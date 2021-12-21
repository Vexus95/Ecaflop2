package info.dmerej.hr;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.annotation.JsonDeserialize;
import com.fasterxml.jackson.databind.annotation.JsonSerialize;

import java.util.Map;

@JsonDeserialize(using = EmployeeDeserializer.class)
@JsonSerialize(using = EmployeeSerializer.class)
public class Employee {
  String name;
  String email;
  String addressLine1;
  String addressLine2;
  String city;
  String zipCode;


  public Employee(
    String name,
    String email,
    String addressLine1,
    String addressLine2,
    String city,
    String zipCode) {
    this.name = name;
    this.email = email;
    this.addressLine1 = addressLine1;
    this.addressLine2 = addressLine2;
    this.city = city;
    this.zipCode = zipCode;
  }

  @Override
  public boolean equals(Object other) {
    if (!(other instanceof Employee)) {
      return false;
    }
    Employee o = (Employee) other;
    return
      o.name.equals(this.name) &&
        o.email.equals(this.email) &&
        o.addressLine1.equals(this.addressLine1) &&
        o.addressLine2.equals(this.addressLine2) &&
        o.city.equals(this.city) &&
        o.zipCode.equals(this.zipCode);
  }

  @Override
  public String toString() {
    return String.format("Employee { name: %s, email : %s, address_line1 : %s, address_line2 : %s, city: %s, zip_code: %s}",
      this.name, this.email, this.addressLine1, this.addressLine2, this.city, this.zipCode);
  }

  public Map<String, Object> asMap() {
    ObjectMapper mapper = new ObjectMapper();
    return mapper.convertValue(this, Map.class);
  }

}
