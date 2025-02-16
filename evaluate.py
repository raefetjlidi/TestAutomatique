import torch
import numpy as np
from sklearn.metrics import confusion_matrix, precision_recall_fscore_support
import seaborn as sns
import matplotlib.pyplot as plt
from nltk_utils import tokenize, stem, bag_of_words
from model import NeuralNet
import json

# Load intents from the JSON file
with open('intents.json', 'r') as f:
    intents = json.load(f)

# Recreate the `tags` and `X_train` (bag-of-words) from the `intents.json`
all_words = []
tags = []
xy = []

# Process the intents
for intent in intents['intents']:
    tag = intent['tag']
    tags.append(tag)
    for pattern in intent['patterns']:
        w = tokenize(pattern)
        all_words.extend(w)
        xy.append((w, tag))

# Ignore punctuation and stem words
ignore_words = ['!', '?', '.', ',']
all_words = [stem(w) for w in all_words if w not in ignore_words]
all_words = sorted(set(all_words))
tags = sorted(set(tags))

# Prepare `X_train` (bag of words) and `y_train` (labels)
X_train = []
y_train = []

for (pattern_sentence, tag) in xy:
    bag = bag_of_words(pattern_sentence, all_words)
    X_train.append(bag)

    label = tags.index(tag)
    y_train.append(label)

X_train = np.array(X_train)

# Define model parameters (same as during training)
input_size = len(X_train[0])  # Number of words in the bag of words
hidden_size = 8  # Same as in training
output_size = len(tags)  # Number of unique tags

# Load the trained model
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = NeuralNet(input_size=input_size, hidden_size=hidden_size, num_classes=output_size).to(device)  # Adjusted initialization
model.load_state_dict(torch.load('model.pth'))
model.eval()  # Set the model to evaluation mode

# Function to predict the response based on user input
def get_response(user_input):
    tokenized_input = tokenize(user_input)
    bag = bag_of_words(tokenized_input, all_words)

    X = torch.tensor(bag, dtype=torch.float32).to(device)

    output = model(X)
    _, predicted = torch.max(output, dim=0)

    tag = tags[predicted.item()]

    for intent in intents['intents']:
        if tag == intent['tag']:
            return intent['responses']

# Function to evaluate the model
def evaluate_model():
    y_pred = []
    y_true = []

    for (pattern_sentence, tag) in xy:
        # Create the bag of words for each sentence
        bag = bag_of_words(pattern_sentence, all_words)

        X = torch.tensor(bag, dtype=torch.float32).to(device)
        output = model(X)
        _, predicted = torch.max(output, dim=0)
        predicted_tag = tags[predicted.item()]

        # Append the results
        y_pred.append(predicted_tag)
        y_true.append(tag)

    # Calculate the confusion matrix
    cm = confusion_matrix(y_true, y_pred)
    print("Confusion Matrix:\n", cm)

    # Calculate precision, recall, and F1 score
    precision, recall, fscore, _ = precision_recall_fscore_support(y_true, y_pred, average='weighted')
    print("Precision:", precision)
    print("Recall:", recall)
    print("F1 Score:", fscore)

    # Visualize the confusion matrix using a heatmap
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=tags, yticklabels=tags)
    plt.title("Confusion Matrix")
    plt.xlabel("Predicted")
    plt.ylabel("True")
    plt.show()

# Evaluate the model
evaluate_model()
