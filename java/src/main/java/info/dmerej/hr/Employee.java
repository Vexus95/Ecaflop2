package info.dmerej.hr;

import com.fasterxml.jackson.databind.ObjectMapper;

import java.util.Map;

public record Employee(String name, String email) {
  public Map<String, Object> asMap() {
    ObjectMapper mapper = new ObjectMapper();
    return mapper.convertValue(this, Map.class);
  }
}
