import gradio as gr
import json
import os

# Simple user database for demonstration (saved as a JSON file)
USER_DB_FILE = "users.json"

# Load users from file or initialize
if not os.path.exists(USER_DB_FILE):
    with open(USER_DB_FILE, "w") as file:
        json.dump({}, file)


def load_users():
    with open(USER_DB_FILE, "r") as file:
        return json.load(file)


def save_users(users):
    with open(USER_DB_FILE, "w") as file:
        json.dump(users, file)


# Function to handle user registration
def register(username, password, verify_password):
    if not username or not password or not verify_password:
        return "Veuillez remplir tous les champs."
    if password != verify_password:
        return "Les mots de passe ne correspondent pas."

    users = load_users()
    if username in users:
        return "Ce nom d'utilisateur est déjà pris."

    users[username] = password
    save_users(users)
    return "Inscription réussie. Veuillez vous connecter."


# Function to handle user login
def login(username, password):
    if not username or not password:
        return "Veuillez remplir les champs de connexion."

    users = load_users()
    if username not in users or users[username] != password:
        return "Nom d'utilisateur ou mot de passe incorrect."

    return gr.update(value="Connexion réussie !", visible=False), gr.update(visible=True)


# Main UI
def accueil_ui():
    css = """
    footer {
        display: none !important;
    }

    body {
        background: linear-gradient(135deg, #0077B6, #03045E);
        font-family: 'Arial', sans-serif;
        color: #FFFFFF;
        height: 100vh;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .gradio-container {
        background: #FFFFFF;
        border-radius: 15px;
        padding: 60px;
        max-width: 800px;
        width: 100%;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
    }

    h3 {
        text-align: center;
        color: #0077B6;
        font-size: 32px;
        margin-bottom: 20px;
    }

    input[type='text'], input[type='password'] {
        width: 100%;
        padding: 12px;
        margin: 10px 0;
        border: 2px solid #0077B6;
        border-radius: 8px;
        font-size: 18px;
    }

    .gr-button {
        width: 100%;
        background-color: #0077B6;
        color: white;
        padding: 15px;
        border: none;
        border-radius: 8px;
        font-size: 18px;
        font-weight: bold;
        cursor: pointer;
        transition: 0.3s;
    }

    .gr-button:hover {
        background-color: #023E8A;
    }
    """

    with gr.Blocks(css=css) as demo:
        with gr.Row():
            gr.Markdown("### Bienvenue chez **QualiMation**")

        with gr.Tab("S'inscrire"):
            username_register = gr.Textbox(label="Nom d'utilisateur")
            password_register = gr.Textbox(label="Mot de passe", type="password")
            verify_password = gr.Textbox(label="Confirmez le mot de passe", type="password")
            register_button = gr.Button("S'inscrire")
            register_status = gr.Text()

            register_button.click(fn=register, inputs=[username_register, password_register, verify_password],
                                  outputs=register_status)

        with gr.Tab("Se connecter"):
            username_login = gr.Textbox(label="Nom d'utilisateur")
            password_login = gr.Textbox(label="Mot de passe", type="password")
            login_button = gr.Button("Se connecter")
            login_status = gr.Text()
            go_to_app = gr.Button("Accéder à l'application", visible=False)

            login_button.click(fn=login, inputs=[username_login, password_login], outputs=[login_status, go_to_app])
            go_to_app.click(fn=None, js="() => window.open('http://127.0.0.1:7788', '_self')")

    return demo


if __name__ == "__main__":
    accueil = accueil_ui()
    accueil.launch()