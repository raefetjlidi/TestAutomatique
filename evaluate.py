import torch
import numpy as np
import json
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, classification_report

from nltk_utils import bag_of_words, tokenize
from model import NeuralNet

# 🔹 Charger le dataset d'entraînement
with open('intents.json', 'r') as f:
    intents = json.load(f)

# 🔹 Charger le modèle et les métadonnées
FILE = "data.pth"
checkpoint = torch.load(FILE)

input_size = checkpoint["input_size"]
hidden_size = checkpoint["hidden_size"]
output_size = checkpoint["output_size"]
all_words = checkpoint["all_words"]
tags = checkpoint["tags"]
model_state = checkpoint["model_state"]

# 🔹 Initialiser le modèle
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

# 🔹 Préparer les données pour l'évaluation
xy = []
y_true = []
y_pred = []

for intent in intents['intents']:
    tag = intent['tag']
    for pattern in intent['patterns']:
        xy.append((pattern, tag))

# 🔹 Tester chaque phrase et stocker les prédictions
for sentence, true_tag in xy:
    # Convertir la phrase en bag-of-words
    bag = bag_of_words(tokenize(sentence), all_words)
    X = torch.tensor(bag, dtype=torch.float32).to(device)

    # Prédiction du modèle
    output = model(X)
    _, predicted_idx = torch.max(output, dim=0)
    predicted_tag = tags[predicted_idx.item()]

    y_true.append(true_tag)
    y_pred.append(predicted_tag)

# 🔹 Calculer la matrice de confusion
cm = confusion_matrix(y_true, y_pred, labels=tags)

# 🔹 Afficher les scores de classification
print("📊 Classification Report:\n")
print(classification_report(y_true, y_pred, target_names=tags))

# 🔹 Afficher la matrice de confusion
plt.figure(figsize=(10, 7))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=tags, yticklabels=tags)
plt.xlabel("Prédictions")
plt.ylabel("Vérité")
plt.title("Matrice de Confusion")
plt.show()
