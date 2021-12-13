package info.dmerej.hr;

import org.junit.Before;
import org.junit.Test;

import java.util.List;

import static org.junit.Assert.*;

public class RepositoryTests {
  private Repository repository;

  @Before
  public void setUp() {
    repository = new Repository(":memory:");
    repository.migrate();
  }

  @Test
  public void canInsertEmployee() {
    Employee bob = new Employee("bob", "bob@domain.tld");

    int id = repository.saveEmployee(bob);
    assertTrue(id >= 0);
  }

  @Test
  public void canRetrieveInsertedEmployee() {
    Employee bob = new Employee("bob", "bob@domain.tld");

    int id = repository.saveEmployee(bob);

    Employee saved = repository.getEmployee(id);
    assertNotNull(saved);
  }

  @Test
  public void canListEmployees() {
    Employee alice = new Employee("alice", "alice@domain.tld");
    Employee bob = new Employee("bob", "bob@domain.tld");

    repository.saveEmployee(bob);
    repository.saveEmployee(alice);

    List<Employee> saved = repository.getEmployees();
    assertEquals(2, saved.size());
  }

}
