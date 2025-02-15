// Fonction pour traduire un texte avec Hugging Face via le backend
async function traduireTexte(texte) {
    try {
        console.log("Envoi de la requête de traduction pour :", texte);
        const response = await fetch('/traduire', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ texte }),
        });

        if (!response.ok) {
            throw new Error("Erreur lors de la traduction");
        }

        const data = await response.json();
        console.log("Traduction reçue :", data.traduction);
        return data.traduction || texte; // Retourne la traduction ou le texte d'origine en cas d'erreur
    } catch (error) {
        console.error("Erreur :", error);
        return texte; // Retourne le texte d'origine en cas d'erreur
    }
}

// Fonction pour traduire toute la page
async function traduirePage() {
    console.log("Traduction en cours...");

    // Sélectionner tous les éléments à traduire
    const elementsATraduire = document.querySelectorAll('h1, h2, p, label, option, button, span, div');

    // Traduire chaque élément
    for (const element of elementsATraduire) {
        const texteOriginal = element.innerText;
        console.log("Texte original :", texteOriginal);

        const texteTraduit = await traduireTexte(texteOriginal);
        console.log("Texte traduit :", texteTraduit);

        element.innerText = texteTraduit;
    }

    console.log("Traduction terminée.");
}