from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

# Load Hugging Face model
model_name = "microsoft/phi-2"

print("🔄 Loading tokenizer and model, this may take a few minutes...")

tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(model_name, trust_remote_code=True)

# Initialize pipeline
generator = pipeline("text-generation", model=model, tokenizer=tokenizer)


def generate_selenium_code(gherkin_step):
    """Convert a Gherkin step into Java Selenium code using AI"""
    prompt = f"Convert the following Gherkin step into Java Selenium code:\n'{gherkin_step}'"

    response = generator(
        prompt,
        max_length=150,
        truncation=True,  # ✅ Explicit truncation
        pad_token_id=tokenizer.eos_token_id,  # ✅ Avoid padding warning
        do_sample=True,
        temperature=0.7
    )

    return response[0]["generated_text"]


if __name__ == "__main__":
    test_step = "Given I open 'https://www.google.com'"
    print("🧠 AI Generated Code:")
    print(generate_selenium_code(test_step))
