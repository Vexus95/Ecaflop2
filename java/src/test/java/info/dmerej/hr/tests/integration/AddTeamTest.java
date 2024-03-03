package info.dmerej.hr.tests.integration;

import okhttp3.FormBody;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import org.junit.jupiter.api.Test;

import java.io.IOException;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.util.*;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

public class AddTeamTest {

    public static final String POSTGRES_URL = "jdbc:postgresql://localhost:5433/hr";

    private static void makeRequest(OkHttpClient client, String url, Map<String, String> body) {
        var formBodyBuilder = new FormBody.Builder();
        for (var entry : body.entrySet()) {
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
            throw new RuntimeException("Error when making POST request for URL: " + url + " : " + e);
        }
    }

    @Test
    void can_create_a_team() {
        var client = new OkHttpClient();

        makeRequest(client, "http://127.0.0.1:8000/reset_db", new HashMap<>());
        makeRequest(client, "http://127.0.0.1:8000/add_team", Map.of("name", "Java devs"));

        try {
            var properties = new Properties();
            properties.setProperty("user", "hr");
            properties.setProperty("password", "hr");
            var connection = DriverManager.getConnection(POSTGRES_URL, properties);
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
            throw new RuntimeException("Could not open DB: " + e);
        }
    }

}
