package info.dmerej.hr;

import org.junit.Before;
import org.junit.Test;

import java.util.List;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertTrue;

public class RepositoryTests {
  private Repository repository;

  @Before
  public void setUp() {
    // Note: this is called before each test, so we get a brand-new
    // database every time, no need to clean it
    repository = new Repository(":memory:");
    repository.migrate();
  }

  @Test
  public void canInsertEmployee() {
    Employee bob = new Employee("bob", "bob@domain.tld");

    SavedEmployee saved = repository.saveEmployee(bob);
    assertTrue(saved.id() >= 0);
  }

  @Test
  public void canRetrieveInsertedEmployee() {
    Employee bob = new Employee("bob", "bob@domain.tld");

    SavedEmployee saved = repository.saveEmployee(bob);

    SavedEmployee actual = repository.getEmployee(saved.id());
    assertEquals(bob, actual.employee());
  }

  @Test
  public void canListEmployees() {
    Employee alice = new Employee("alice", "alice@domain.tld");
    Employee bob = new Employee("bob", "bob@domain.tld");

    repository.saveEmployee(bob);
    repository.saveEmployee(alice);

    List<SavedEmployee> saved = repository.getEmployees();
    assertEquals(2, saved.size());
  }

  @Test
  public void canUpdateEmployeeName() {
    Employee alice = new Employee("alice", "alice@domain.tld");
    SavedEmployee saved = repository.saveEmployee(alice);
    int aliceId = saved.id();

    Employee payload = new Employee("new name", "alice@domain.tld");
    repository.updateEmployee(aliceId, payload);

    SavedEmployee actual = repository.getEmployee(aliceId);
    assertEquals("new name", actual.employee().name());
  }

  @Test
  public void canDeleteEmployees() {
    Employee alice = new Employee("alice", "alice@domain.tld");
    repository.saveEmployee(alice);

    Employee bob = new Employee("alice", "alice@domain.tld");
    repository.saveEmployee(bob);

    int deleted = repository.deleteEmployees();

    assertEquals(2, deleted);
  }

}
