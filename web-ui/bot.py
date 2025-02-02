import os
from jinja2 import Template

# Read Gherkin scenario from file
def read_gherkin_from_file(file_path):
    with open(file_path, "r") as file:
        return file.read()

# Save generated Java code to file
def save_java_code(file_name, code):
    os.makedirs("generated_code", exist_ok=True)  # Create the folder if it doesn't exist
    with open(f"generated_code/{file_name}", "w") as file:
        file.write(code)

# Generate Java code from Gherkin scenario
def generate_java_code(scenario):
    # Parse Gherkin steps (simplified for now)
    steps = []
    for line in scenario.split("\n"):
        if line.strip().startswith(("Given", "When", "Then", "And")):
            steps.append(line.strip())

    # Map steps to Selenium actions (simplified for now)
    selenium_steps = []
    for step in steps:
        if "I am on the" in step:
            selenium_steps.append('driver.get("https://example.com/login");')
        elif "I enter" in step:
            selenium_steps.append('driver.findElement(By.id("username")).sendKeys("testuser");')
            selenium_steps.append('driver.findElement(By.id("password")).sendKeys("testpass");')
        elif "I click" in step:
            selenium_steps.append('driver.findElement(By.id("login-button")).click();')
        elif "I should be redirected" in step:
            selenium_steps.append('assert driver.getCurrentUrl().equals("https://example.com/dashboard");')

    # Java code template
    java_template = """
    import org.openqa.selenium.By;
    import org.openqa.selenium.WebDriver;
    import org.openqa.selenium.chrome.ChromeDriver;
    import org.junit.Test;
    import org.junit.Before;
    import org.junit.After;
    import static org.junit.Assert.*;

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

    # Render the template
    template = Template(java_template)
    return template.render(test_name="LoginTest", method_name="testLogin", steps="\n".join(selenium_steps))

# Main script
if __name__ == "__main__":
    # Read the Gherkin scenario
    scenario = read_gherkin_from_file("gherkin_scenarios/login.feature")

    # Generate Java code
    java_code = generate_java_code(scenario)

    # Save the generated code
    save_java_code("LoginTest.java", java_code)

    print("Java code generated successfully! Check the 'generated_code' folder.")