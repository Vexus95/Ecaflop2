package info.dmerej.hr;

import java.util.Map;

public record SavedEmployee(int id, Employee employee) {
  Map<String, Object> asMap() {
    Map<String, Object> res = employee.asMap();
    res.put("id", id);
    return res;
  }
}
