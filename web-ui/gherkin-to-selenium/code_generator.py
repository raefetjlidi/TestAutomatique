from jinja2 import Template

java_template = """import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;

public class GeneratedTest {
    public static void main(String[] args) {
        System.setProperty("webdriver.chrome.driver", "path/to/chromedriver");
        WebDriver driver = new ChromeDriver();

        try {
            {{ steps_code }}

        } finally {
            driver.quit();
        }
    }
}
"""

def generate_java_class(selenium_code):
    template = Template(java_template)
    return template.render(steps_code=selenium_code)
