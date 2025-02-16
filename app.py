import random
import json
import torch
import tkinter as tk
from tkinter import scrolledtext
from model import NeuralNet
from nltk_utils import bag_of_words, tokenize

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open('intents.json', 'r') as json_data:
    intents = json.load(json_data)

FILE = "data.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

bot_name = "QualiAssist"


def get_response(msg):
    sentence = tokenize(msg)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)

    output = model(X)
    _, predicted = torch.max(output, dim=1)

    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]
    if prob.item() > 0.75:
        for intent in intents['intents']:
            if tag == intent["tag"]:
                return random.choice(intent['responses'])

    return "I do not understand..."


# GUI Implementation
def send_message():
    user_input = user_entry.get()
    if user_input.strip() == "":
        return

    chat_area.configure(state=tk.NORMAL)
    chat_area.insert(tk.END, "Client: " + user_input + "\n", "user")
    user_entry.delete(0, tk.END)

    response = get_response(user_input)
    chat_area.insert(tk.END, bot_name + ": " + response + "\n", "bot")
    chat_area.configure(state=tk.DISABLED)
    chat_area.yview(tk.END)


def on_enter(event):
    send_message()


# Create main application window
root = tk.Tk()
root.title("QualiAssist GUI")
root.geometry("500x500")

chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, state=tk.DISABLED, height=20, width=55)
chat_area.pack(padx=10, pady=10)
chat_area.tag_config("user", foreground="blue")
chat_area.tag_config("bot", foreground="green")

user_entry = tk.Entry(root, width=50)
user_entry = tk.Entry(root, width=50)
user_entry.pack(padx=10, pady=5)
user_entry.bind("<Return>", on_enter)

send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack(pady=5)

root.mainloop()
