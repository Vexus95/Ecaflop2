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
        email TEXT NOT NULL,
        address_line1 TEXT NOT NULL,
        address_line2 TEXT NOT NULL,
        city TEXT NOT NULL,
        zip_code TEXT NOT NULL
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
      PreparedStatement statement = connection.prepareStatement("""
          INSERT INTO
            employee(name, email, address_line1, address_line2, city, zip_code)
          VALUES
            (?, ?, ?, ?, ?, ?)
        """);
      statement.setString(1, employee.name);
      statement.setString(2, employee.email);
      statement.setString(3, employee.addressLine1);
      statement.setString(4, employee.addressLine2);
      statement.setString(5, employee.city);
      statement.setString(6, employee.zipCode);
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
      PreparedStatement statement = connection.prepareStatement("""
        SELECT
          name, email, address_line1, address_line2, city, zip_code
        FROM
          employee
        WHERE id = ?
        """);
      statement.setInt(1, id);
      ResultSet set = statement.executeQuery();
      String name = set.getString(1);
      String email = set.getString(2);
      String addressLine1 = set.getString(3);
      String addressLine2 = set.getString(4);
      String city = set.getString(5);
      String zipCode = set.getString(6);
      Employee employee = new Employee(name, email, addressLine1, addressLine2, city, zipCode);
      return new SavedEmployee(id, employee);
    } catch (SQLException e) {
      throw new RuntimeException("Could not save employee: " + e);
    }
  }

  public List<SavedEmployee> getEmployees() {
    try {
      Statement statement = connection.createStatement();
      ResultSet set = statement.executeQuery("""
        SELECT
          id, name, email, address_line1, address_line2, city, zip_code
        FROM 
          employee
        """
      );
      ArrayList<SavedEmployee> res = new ArrayList<>();
      while (set.next()) {
        Integer id = set.getInt(1);
        String name = set.getString(2);
        String email = set.getString(3);
        String addressLine1 = set.getString(4);
        String addressLine2 = set.getString(5);
        String city = set.getString(6);
        String zipCode = set.getString(7);
        Employee employee = new Employee(name, email, addressLine1, addressLine2, city, zipCode);
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
        UPDATE
          employee
        SET
          name=?, email=?, address_line1=?, address_line2=?, city=?, zip_code=?
        WHERE
           id = ?
        """);
      statement.setString(1, employee.name);
      statement.setString(2, employee.email);
      statement.setString(3, employee.addressLine1);
      statement.setString(4, employee.addressLine2);
      statement.setString(5, employee.city);
      statement.setString(6, employee.zipCode);
      statement.setInt(7, id);
      statement.execute();
    } catch (SQLException e) {
      throw new RuntimeException("Could not update employee: " + e);
    }
  }

  public void deleteEmployee(int id) {
    try {
      PreparedStatement statement = connection.prepareStatement("""
        DELETE FROM employee WHERE id = ?
        """);
      statement.setInt(1, id);
      statement.execute();
    } catch (SQLException e) {
      throw new RuntimeException("Could not delete employee: " + e);
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
