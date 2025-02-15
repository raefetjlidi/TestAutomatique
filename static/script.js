// Function to translate the entire page (paragraph, keywords, employee table)
async function traduireTout() {
    try {
        console.log("Traduction de toute la page en cours...");

        // Translate paragraph text
        const paragraphElement = document.getElementById('paragraph');
        const paragraphText = paragraphElement.innerText;

        const paragraphTranslation = await traduireTexteBatch([paragraphText]);
        paragraphElement.innerText = paragraphTranslation[0];

        // Translate select dropdown options (keywords)
        const selectElement = document.getElementById('keywordsSelect');
        const optionElements = Array.from(selectElement.options);
        const keywords = optionElements.map(option => option.textContent);

        const keywordsTranslations = await traduireTexteBatch(keywords);
        optionElements.forEach((option, index) => {
            option.textContent = keywordsTranslations[index];
        });

        // Translate employee table rows
        const employeeRows = Array.from(document.getElementById("employeeTableBody").rows);
        for (const row of employeeRows) {
            const nameCell = row.cells[0].innerText;
            const descriptionCell = row.cells[1].innerText;
            const jobCell = row.cells[2].innerText;

            const [translatedName, translatedDescription, translatedJob] = await traduireTexteBatch([nameCell, descriptionCell, jobCell]);

            row.cells[0].innerText = translatedName;
            row.cells[1].innerText = translatedDescription;
            row.cells[2].innerText = translatedJob;
        }

        console.log("Traduction terminée.");
    } catch (error) {
        console.error("Erreur lors de la traduction:", error);
    }
}

// Function to send texts for translation
async function traduireTexteBatch(textes) {
    try {
        const response = await fetch('/traduire_batch', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ textes }),
        });

        if (!response.ok) {
            throw new Error("Erreur lors de la traduction");
        }

        const data = await response.json();
        return data.traductions || textes; // Return translations or original text in case of error
    } catch (error) {
        console.error("Erreur :", error);
        return textes; // Return original texts if there is an error
    }
}