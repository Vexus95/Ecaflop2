package info.dmerej.hr;

import java.sql.*;
import java.util.ArrayList;
import java.util.List;

public class Repository {
  private final Connection connection;

  public Repository(String dbPath) {
    try {
      connection = DriverManager.getConnection("jdbc:sqlite:" + dbPath);
    } catch (SQLException e) {
      throw new RuntimeException("Could not create connection: " + e);
    }
  }

  public void migrate() {
    System.out.println("Migrating database ...");
    try {
      Statement statement = connection.createStatement();
      statement.execute("""
        CREATE TABLE employee(
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT NOT NULL
        )
        """
      );
    } catch (SQLException e) {
      throw new RuntimeException("Could not migrate db: " + e);
    }
    System.out.println("Done migrating database");
  }

  public SavedEmployee saveEmployee(Employee employee) {
    try {
      PreparedStatement statement = connection.prepareStatement("INSERT INTO employee(name, email) VALUES (?, ?)");
      statement.setString(1, employee.name());
      statement.setString(2, employee.email());
      statement.execute();
    } catch (SQLException e) {
      throw new RuntimeException("Could not save employee: " + e);
    }

    try {
      Statement statement = connection.createStatement();
      ResultSet res = statement.executeQuery("SELECT last_insert_rowid() AS id");
      int id = res.getInt(1);
      return new SavedEmployee(id, employee);
    } catch (SQLException e) {
      throw new RuntimeException("Could not get employee id " + e);
    }
  }

  public SavedEmployee getEmployee(int id) {
    try {
      PreparedStatement statement = connection.prepareStatement("SELECT name, email FROM employee WHERE id = ?");
      statement.setInt(1, id);
      ResultSet set = statement.executeQuery();
      String name = set.getString(1);
      String email = set.getString(2);
      Employee employee = new Employee(name, email);
      return new SavedEmployee(id, employee);
    } catch (SQLException e) {
      throw new RuntimeException("Could not save employee: " + e);
    }
  }

  public List<SavedEmployee> getEmployees() {
    try {
      Statement statement = connection.createStatement();
      ResultSet resultSet = statement.executeQuery("SELECT id, name, email FROM employee");
      ArrayList<SavedEmployee> res = new ArrayList<>();
      while (resultSet.next()) {
        Integer id = resultSet.getInt(1);
        String name = resultSet.getString(2);
        String email = resultSet.getString(3);
        Employee employee = new Employee(name, email);
        SavedEmployee savedEmployee = new SavedEmployee(id, employee);
        res.add(savedEmployee);
      }
      return res;
    } catch (SQLException e) {
      throw new RuntimeException("Could not fetch employees: " + e);
    }
  }

  public void updateEmployee(int id, Employee employee) {
    try {
      PreparedStatement statement = connection.prepareStatement("""
        UPDATE employee SET name=?, email=? WHERE id = ?
        """);
      statement.setString(1, employee.name());
      statement.setString(2, employee.email());
      statement.setInt(3, id);
      statement.execute();
    } catch (SQLException e) {
      throw new RuntimeException("Could not update employee: " + e);
    }
  }

  public int deleteEmployees() {
    try {
      Statement statement = connection.createStatement();
      return statement.executeUpdate("DELETE FROM employee");
    } catch (SQLException e) {
      throw new RuntimeException("Could not update employee: " + e);
    }
  }
}
