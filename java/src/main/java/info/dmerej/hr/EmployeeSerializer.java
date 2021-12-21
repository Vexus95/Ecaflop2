package info.dmerej.hr;

import com.fasterxml.jackson.core.JsonGenerator;
import com.fasterxml.jackson.databind.SerializerProvider;
import com.fasterxml.jackson.databind.ser.std.StdSerializer;

import java.io.IOException;

public class EmployeeSerializer extends StdSerializer<Employee> {
  public EmployeeSerializer() {
    this(null);
  }

  public EmployeeSerializer(Class<Employee> t) {
    super(t);
  }

  @Override
  public void serialize(Employee value, JsonGenerator gen, SerializerProvider provider) throws IOException {
    gen.writeStartObject();
    gen.writeStringField("name", value.name);
    gen.writeStringField("email", value.email);
    gen.writeStringField("address_line1", value.addressLine1);
    gen.writeStringField("address_line2", value.addressLine2);
    gen.writeStringField("city", value.city);
    gen.writeStringField("zip_code", value.zipCode);
    gen.writeEndObject();
  }
}
