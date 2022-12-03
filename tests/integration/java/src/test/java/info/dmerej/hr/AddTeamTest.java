package info.dmerej.hr;

import okhttp3.FormBody;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import org.junit.jupiter.api.Test;

import java.io.IOException;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

public class AddTeamTest {
  @Test
  void can_create_a_team() {
    var dbPath = "../../../backend/db.sqlite3";

    var client = new OkHttpClient();

    makeRequest(client, "http://127.0.0.1:8000/reset_db", new HashMap<>());
    makeRequest(client, "http://127.0.0.1:8000/add_team", Map.of("name", "Java devs"));

    try {
      var connection = DriverManager.getConnection("jdbc:sqlite:" + dbPath);
      var query = "SELECT name FROM hr_team";
      var statement = connection.prepareStatement(query);
      var result = statement.executeQuery();
      var actual = new ArrayList<String>();
      while (result.next()) {
        actual.add(result.getString(1));
      }
      var expected = List.of("Java devs");
      assertEquals(expected, actual.stream().toList());
    } catch (SQLException e) {
      throw new RuntimeException("Could not open DB: " + e.toString());
    }
  }

  private static void makeRequest(OkHttpClient client, String url, Map<String, String> body) {
    // Add team
    var formBodyBuilder = new FormBody.Builder();
    for (var entry: body.entrySet()) {
      formBodyBuilder.add(entry.getKey(), entry.getValue());
    }
    var formBody = formBodyBuilder.build();

    var request = new Request.Builder()
      .url(url)
      .post(formBody)
      .build();

    try {
      var response = client.newCall(request).execute();
      assertTrue(response.isSuccessful());
    } catch (IOException e) {
      throw new RuntimeException("Error when making POST request for URL: " + url + " : " + e.toString());
    }
  }

}
