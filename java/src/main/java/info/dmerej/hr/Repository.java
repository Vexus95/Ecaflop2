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

  public int saveEmployee(Employee employee) {
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
      return res.getInt(1);
    } catch (SQLException e) {
      throw new RuntimeException("Could not get employee id " + e);
    }
  }

  public Employee getEmployee(int id) {
    try {
      PreparedStatement statement = connection.prepareStatement("SELECT name, email FROM employee WHERE id = ?");
      statement.setInt(1, id);
      ResultSet set = statement.executeQuery();
      String name = set.getString(1);
      String email = set.getString(2);
      return new Employee(name, email);
    } catch (SQLException e) {
      throw new RuntimeException("Could not save employee: " + e);
    }
  }

  public List<Employee> getEmployees() {
    try {
      Statement statement = connection.createStatement();
      ResultSet resultSet = statement.executeQuery("SELECT name, email FROM employee");
      ArrayList<Employee> res = new ArrayList<>();
      while (resultSet.next()) {
        String name = resultSet.getString(1);
        String email = resultSet.getString(2);
        Employee employee = new Employee(name, email);
        res.add(employee);
      }
      return res;
    } catch (SQLException e) {
      throw new RuntimeException("Could not fetch employees: " + e);
    }
  }
}
