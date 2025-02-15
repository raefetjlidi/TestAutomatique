from flask import Flask, render_template, request, jsonify
from deep_translator import GoogleTranslator
import json

app = Flask(__name__)

# Glossary for custom word replacements
glossary = {
    "essentiels": "mouhema",
    "concepts": "olelele"
}

# Function to read data from JSON files
def load_json_data(filename):
    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)

# Load employe.json and keywords.json
employes_data = load_json_data("data/employe.json")
keywords_data = load_json_data("data/keywords.json")

# Combine both data into a single data structure
combined_data = {
    "employes": employes_data,
    "keywords": keywords_data["keywords"]
}

# AI Translation Function using deep_translator
def translate_text(text):
    # Translate French to English using deep_translator (Google)
    translated_text = GoogleTranslator(source='fr', target='en').translate(text)

    # Apply glossary replacements
    for word, replacement in glossary.items():
        translated_text = translated_text.replace(word, replacement)

    return translated_text

# Route to serve homepage with AI-translated title and combined data
@app.route("/")
def home():
    title_fr = "Bienvenue sur notre site sur les normes ISO"
    title_en = translate_text(title_fr)  # AI translation
    return render_template("index.html", title=title_en, combined_data=combined_data)

# Route to handle AI translation for batch text
@app.route("/traduire_batch", methods=["POST"])
def traduire_batch():
    data = request.json
    textes = data.get("textes", [])

    # Translate each text in the list
    traductions = [translate_text(texte) for texte in textes]
    return jsonify({"traductions": traductions})


@app.route("/traduire_iso", methods=["POST"])
def translate_iso():
    translated_list = [
        {
            "id": item["id"],
            "mot": translate_text(item["mot"]),
            "definition": translate_text(item["definition"])
        }
        for item in combined_data['employes']  # Example, adapt as needed
    ]
    return jsonify({"translated_list": translated_list})
if __name__ == "__main__":
    app.run(debug=True)
