import re

def parse_gherkin(gherkin_text):
    """Extract Given, When, Then, And steps from a Gherkin scenario"""
    pattern = r"(Given|When|Then|And)\s+(.*)"
    matches = re.findall(pattern, gherkin_text, re.IGNORECASE)

    structured_steps = [{"step_type": step[0], "action": step[1]} for step in matches]
    return structured_steps
