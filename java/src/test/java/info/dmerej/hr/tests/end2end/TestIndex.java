package info.dmerej.hr.tests.end2end;

import com.microsoft.playwright.BrowserType;
import com.microsoft.playwright.Playwright;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertTrue;

public class TestIndex {
    @Test
    void show_index() {
        var playwright = Playwright.create();
        var options = new BrowserType.LaunchOptions().setHeadless(false);
        // if you need to better see what's going on ...
        // .setSlowMo(1000);
        var browser = playwright.chromium().launch(options);
        var page = browser.newPage();
        page.navigate("http://127.0.0.1:8000");
        var contents = page.content();
        assertTrue(contents.contains("List employees"), "Home page should contain a 'List employees' link");
        playwright.close();

    }
}
