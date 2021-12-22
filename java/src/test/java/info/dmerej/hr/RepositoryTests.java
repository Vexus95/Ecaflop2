package info.dmerej.hr;

import org.junit.Before;
import org.junit.Test;

import java.util.List;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertTrue;


public class RepositoryTests {
  static
  private Repository repository;
  private Employee alice;
  private Employee bob;

  @Before
  public void setUp() {
    // Note: this is called before each test, so we get a brand-new
    // database every time, no need to clean it
    repository = new Repository(":memory:");
    repository.migrate();

    alice = new Employee(
      "alice",
      "alice@domain.tld",
      "226 Sweeney Manors Suite",
      "Suite 41",
      "New York",
      "45378"
    );

    bob = new Employee(
      "bob",
      "bob@domain.tld",
      "55211 Perez Ville",
      "Apt. 816",
      "Los Angeles",
      "44096"
    );
  }

  @Test
  public void canInsertEmployee() {
    SavedEmployee saved = repository.saveEmployee(bob);
    assertTrue(saved.id() >= 0);
  }

  @Test
  public void canRetrieveInsertedEmployee() {
    SavedEmployee saved = repository.saveEmployee(bob);

    SavedEmployee actual = repository.getEmployee(saved.id());
    assertEquals(bob, actual.employee());
  }

  @Test
  public void canListEmployees() {
    repository.saveEmployee(alice);
    repository.saveEmployee(bob);

    List<SavedEmployee> saved = repository.getEmployees();
    assertEquals(2, saved.size());

    SavedEmployee savedAlice = saved.get(0);
    assertEquals(savedAlice.employee(), alice);
  }

  @Test
  public void canUpdateEmployeeName() {
    SavedEmployee saved = repository.saveEmployee(alice);
    int aliceId = saved.id();

    Employee payload = alice;
    payload.name = "new name";
    repository.updateEmployee(aliceId, payload);

    SavedEmployee actual = repository.getEmployee(aliceId);
    assertEquals("new name", actual.employee().name);
  }

  @Test
  public void canDeleteEmployees() {
    repository.saveEmployee(alice);
    repository.saveEmployee(bob);

    int deleted = repository.deleteEmployees();

    assertEquals(2, deleted);
  }

}
