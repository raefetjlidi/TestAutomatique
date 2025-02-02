
    import org.openqa.selenium.By;
    import org.openqa.selenium.WebDriver;
    import org.openqa.selenium.chrome.ChromeDriver;
    import org.junit.Test;
    import org.junit.Before;
    import org.junit.After;
    import static org.junit.Assert.*;

    public class LoginTest {
        WebDriver driver;

        @Before
        public void setUp() {
            driver = new ChromeDriver();
        }

        @Test
        public void testLogin() {
            driver.get("https://example.com/login");
driver.findElement(By.id("username")).sendKeys("testuser");
driver.findElement(By.id("password")).sendKeys("testpass");
driver.findElement(By.id("username")).sendKeys("testuser");
driver.findElement(By.id("password")).sendKeys("testpass");
driver.findElement(By.id("username")).sendKeys("testuser");
driver.findElement(By.id("password")).sendKeys("testpass");
driver.findElement(By.id("login-button")).click();
assert driver.getCurrentUrl().equals("https://example.com/dashboard");
        }

        @After
        public void tearDown() {
            driver.quit();
        }
    }
    