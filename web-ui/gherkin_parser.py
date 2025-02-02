def parse_gherkin(scenario):
    steps = []
    for line in scenario.split("\n"):
        line = line.strip()
        if line.startswith(("Given", "When", "Then", "And")):
            steps.append(line)
    return steps

# Example usage
scenario = """
Given I am on the login page
When I enter "testuser" and "testpass"
And I click the login button
Then I should be redirected to the dashboard
"""

steps = parse_gherkin(scenario)
for step in steps:
    print(step)