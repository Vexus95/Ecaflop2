package info.dmerej.hr;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
public class EmployeeController {
  private final Repository repository;

  public EmployeeController(Repository repository) {
    this.repository = repository;
  }

  @GetMapping("api/v1/employees")
  public List<Employee> getEmployees() {
    return repository.getEmployees();
  }


  @GetMapping("/greeting")
  public Greeting greeting(@RequestParam(value = "name", defaultValue = "World") String name) {
    return new Greeting(1, "world");
  }
}
