from flask import Flask, render_template, request, jsonify
from transformers import MarianMTModel, MarianTokenizer

app = Flask(__name__)

# Load AI translation model (French → English)
model_name = "Helsinki-NLP/opus-mt-fr-en"
tokenizer = MarianTokenizer.from_pretrained(model_name)
model = MarianMTModel.from_pretrained(model_name)

# Glossary for custom word replacements
glossary = {
    "essentiels": "mouhema",
    "concepts": "olelele"
}

# ISO Standards List
iso_standards = [
    {"id": 1, "mot": "Norme internationale pour les systèmes de management de la qualité.", "definition": "ISO 9001"},
    {"id": 2, "mot": "Norme internationale pour les systèmes de management environnemental.", "definition": "ISO 14001"},
    {"id": 3, "mot": "ISO 45001", "definition": "Norme internationale pour les systèmes de management de la santé et de la sécurité au travail."},
    {"id": 4, "mot": "ISO 27001", "definition": "Norme internationale pour les systèmes de management de la sécurité de l'information."}
]

# AI Translation Function
def translate_text(text):
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    translated = model.generate(**inputs)
    translated_text = tokenizer.batch_decode(translated, skip_special_tokens=True)[0]

    # Apply glossary replacements
    for word, replacement in glossary.items():
        translated_text = translated_text.replace(word, replacement)

    return translated_text

# Route to serve homepage with AI-translated title
@app.route("/")
def home():
    title_fr = "Bienvenue sur notre site sur les normes ISO"
    title_en = translate_text(title_fr)  # AI translation
    return render_template("index.html", title=title_en, iso_standards=iso_standards)

# Route to handle AI translation
@app.route("/translate", methods=["POST"])
def translate():
    data = request.json
    text = data.get("text", "")

    translated_text = translate_text(text)
    return jsonify({"translated_text": translated_text})

# Route to translate ISO standards list
@app.route("/translate_iso", methods=["POST"])
def translate_iso():
    translated_list = [
        {
            "id": item["id"],
            "mot": translate_text(item["mot"]),
            "definition": translate_text(item["definition"])
        }
        for item in iso_standards
    ]
    return jsonify({"translated_list": translated_list})

if __name__ == "__main__":
    app.run(debug=True)
