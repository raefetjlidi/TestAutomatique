from gherkin_parser import parse_gherkin
from code_generator import generate_java_class
from ai_model import generate_selenium_code

# 🔽 🔽 🔽 PUT YOUR INPUT HERE 🔽 🔽 🔽
gherkin_text = """
Scenario: Recherche du Logitech Superlight 2
Given j'ouvre "https://www.google.com"
When je saisis "mega pc"
Then je clique sur recherche
And je clique sur le premier site web
And j'écris "logitech superlight2"
And je clique sur recherche
Then je vérifie que le nom est "superlight2"
"""

# Step 1: Extract structured steps from Gherkin
parsed_steps = parse_gherkin(gherkin_text)

# Step 2: Generate Selenium Java code for each step using AI
selenium_code_lines = []
for step in parsed_steps:
    ai_code = generate_selenium_code(step["action"])
    selenium_code_lines.append(ai_code)

# Step 3: Assemble the full Java test class
final_java_code = generate_java_class("\n        ".join(selenium_code_lines))

# Step 4: Save the generated Java file
with open("GeneratedTest.java", "w", encoding="utf-8") as file:
    file.write(final_java_code)

print("✅ Java Selenium test case generated successfully!")
print("📄 Check 'GeneratedTest.java' for the output.")
