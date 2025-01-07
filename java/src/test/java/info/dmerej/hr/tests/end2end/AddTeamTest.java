package info.dmerej.hr.tests.end2end;

import com.microsoft.playwright.Browser;
import com.microsoft.playwright.BrowserType;
import com.microsoft.playwright.Playwright;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertTrue;

public class AddTeamTest {
    @Test
    void test_add_team() {
        // Use playwright driver to get a browser and open a new page
        var playwright = Playwright.create();
        var launchOptions = new BrowserType.LaunchOptions().setHeadless(false)
                .setSlowMo(1000); // Remove this when you're done debugging
        var browser = playwright.chromium().launch(launchOptions);

        // Set base URL for the new context
        var contextOptions = new Browser.NewContextOptions();
        contextOptions.setBaseURL("https://a.lsi1.hr.dmerej.info");
        var context = browser.newContext(contextOptions);

        var page = context.newPage();

        // Reset database
        page.navigate("/reset_db");
        var proceedButton = page.locator("button:has-text('proceed')");
        proceedButton.click();
        page.navigate("/");

        // Add a new team
        page.navigate("/add_team");
        var nameInput = page.locator("input[name=\"name\"]");
        var teamName = "my team";
        nameInput.fill(teamName);
        page.click("text='Add'");

        // Check that the team has been added
        page.navigate("/teams");

        // Check the new team is there
        String selector = String.format("td:has-text('%s')", teamName);
        var isVisible = page.isVisible(selector);
        assertTrue(isVisible);
    }
}
