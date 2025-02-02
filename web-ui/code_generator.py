from jinja2 import Template

# Java code template
java_template = """
public class {{ test_name }} {
    WebDriver driver;

    @Before
    public void setUp() {
        driver = new ChromeDriver();
    }

    @Test
    public void {{ method_name }}() {
        {{ steps }}
    }

    @After
    public void tearDown() {
        driver.quit();
    }
}
"""

def generate_java_code(test_name, method_name, steps):
    template = Template(java_template)
    return template.render(test_name=test_name, method_name=method_name, steps="\n".join(steps))

# Example usage
test_name = "LoginTest"
method_name = "testLogin"
steps = [
    'driver.get("https://example.com/login");',
    'driver.findElement(By.id("username")).sendKeys("testuser");',
    'driver.findElement(By.id("password")).sendKeys("testpass");',
    'driver.findElement(By.id("login-button")).click();',
    'assert driver.getCurrentUrl().equals("https://example.com/dashboard");'
]

java_code = generate_java_code(test_name, method_name, steps)
print(java_code)