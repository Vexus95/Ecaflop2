package info.dmerej.hr;

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

    public static final String DATABASE_PATH = "jdbc:sqlite:../backend/db.sqlite3";

    @Test
    void can_create_a_team() {
        // Call the /add_team route
        var client = new OkHttpClient();

        var formBodyBuilder = new FormBody.Builder();
        for (var entry : Map.of("name", "Java devs").entrySet()) {
            formBodyBuilder.add(entry.getKey(), entry.getValue());
        }
        var formBody = formBodyBuilder.build();

        var request = new Request.Builder()
            .url("http://127.0.0.1:8000/add_team")
            .post(formBody)
            .build();

        try {
            var response = client.newCall(request).execute();
            assertTrue(response.isSuccessful());
        } catch (IOException e1) {
            throw new RuntimeException("Error when making POST request for URL: " + "http://127.0.0.1:8000/add_team" + " : " + e1);
        }


        // Verify the list of teams
        try {
            var connection = DriverManager.getConnection(DATABASE_PATH);
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
