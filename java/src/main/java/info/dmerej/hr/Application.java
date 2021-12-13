package info.dmerej.hr;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;

import java.io.File;

@SpringBootApplication
public class Application {

  public static void main(String[] args) {
    SpringApplication.run(Application.class, args);
  }

  @Bean
  public Repository repository() {
    File dbPath = new File("hr.sqlite3");
    Repository repository;
    if (dbPath.exists()) {
      // We can't instantiate the repository before checking the db path
      // exists, because the driver creates the file when opening the db.
      repository = new Repository(dbPath.getPath());
    } else {
      repository = new Repository(dbPath.getPath());
      repository.migrate();
    }
    return repository;
  }

}
