package info.dmerej.hr;

import org.springframework.web.bind.annotation.*;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;


@RestController
public class EmployeeController {
  private final Repository repository;

  public EmployeeController(Repository repository) {
    this.repository = repository;
  }

  @GetMapping("api/v1/employees")
  public List<Map<String, Object>> getEmployees() {
    List<SavedEmployee> savedEmployees = repository.getEmployees();
    List<Map<String, Object>> res = new ArrayList<>();
    for (SavedEmployee s : savedEmployees) {
      res.add(s.asMap());
    }
    return res;
  }

  @DeleteMapping("api/v1/employees")
  public Map<String, Object> deleteEmployees() {
    int deleted = repository.deleteEmployees();
    return Map.of("deleted", deleted);
  }

  @PutMapping("api/v1/employee")
  public Map<String, Object> createEmployee(@RequestBody Employee employee) {
    SavedEmployee savedEmployee = repository.saveEmployee(employee);
    return Map.of("employee", savedEmployee.asMap());
  }

  @GetMapping("api/v1/employee/{id}")
  public Map<String, Object> getEmployeeById(@PathVariable("id") int id) {
    SavedEmployee savedEmployee = repository.getEmployee(id);
    return Map.of("employee", savedEmployee.asMap());
  }

  @PutMapping("api/v1/employee/{id}")
  public Map<String, Object> updateEmployee(@PathVariable("id") int id, @RequestBody Employee employee) {
    repository.updateEmployee(id, employee);
    SavedEmployee savedEmployee = new SavedEmployee(id, employee);
    return Map.of("employee", savedEmployee.asMap());
  }
}
