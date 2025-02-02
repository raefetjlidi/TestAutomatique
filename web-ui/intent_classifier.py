from transformers import pipeline

# Load a pre-trained model for text classification
classifier = pipeline("text-classification", model="distilbert-base-uncased")

# Define a mapping of intents to Selenium actions
intent_mapping = {
    "navigate": "driver.get(\"page_url\");",
    "input": "driver.findElement(By.id(\"field_id\")).sendKeys(\"value\");",
    "click": "driver.findElement(By.id(\"element_id\")).click();",
    "validate": "assert driver.getCurrentUrl().equals(\"expected_url\");"
}

def classify_intent(step):
    result = classifier(step)[0]
    return result["label"]

# Example usage
step = "Given I am on the login page"
intent = classify_intent(step)
print(f"Step: {step} -> Intent: {intent} -> Action: {intent_mapping.get(intent, 'Unknown')}")