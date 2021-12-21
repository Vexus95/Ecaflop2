package info.dmerej.hr;

import com.fasterxml.jackson.core.JsonParser;
import com.fasterxml.jackson.databind.DeserializationContext;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.deser.std.StdDeserializer;

import java.io.IOException;

public class EmployeeDeserializer extends StdDeserializer<Employee> {
  public EmployeeDeserializer() {
    this(null);
  }

  protected EmployeeDeserializer(Class<?> vc) {
    super(vc);
  }

  @Override
  public Employee deserialize(JsonParser p, DeserializationContext c) throws IOException {
    JsonNode node = p.getCodec().readTree(p);
    String name = node.get("name").asText();
    String email = node.get("email").asText();
    String address_line1 = node.get("address_line1").asText();
    String address_line2 = node.get("address_line2").asText();
    String city = node.get("city").asText();
    String zip_code = node.get("zip_code").asText();
    return new Employee(name, email, address_line1, address_line2, city, zip_code);
  }
}
