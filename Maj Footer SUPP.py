import os
from bs4 import BeautifulSoup

# Charger index.html
with open("index.html", "r", encoding="utf-8") as f:
    index_soup = BeautifulSoup(f, "html.parser")

# Récupérer la balise <nav class="sidebar">
nav = index_soup.find("nav", class_="sidebar")
import os
import re

# Identifiant pour l'insertion
insertion_marker_start = "<!-- CONTENU PERSONNALISÉ DÉBUT -->"
	<div id="footer-container"></div>
	<script>
		fetch("includes/footer.html")
			.then(response => response.text())
			.then(data => {
			document.getElementById("footer-container").innerHTML = data;
			})
			.catch(error => console.error("Erreur lors du chargement du pied de page :", error));
	</script>
	
insertion_marker_end = "<!-- CONTENU PERSONNALISÉ FIN -->"

# Lire la référence (premier fichier trouvé avec le bloc entre </main> et </body>)
reference_content = None

# Lister les fichiers HTML à la racine
html_files = [f for f in os.listdir('.') if f.endswith('.html') and os.path.isfile(f)]

# Trouver un contenu de référence à insérer
for file in html_files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
        match = re.search(r'</main>(.*?)</body>', content, re.DOTALL | re.IGNORECASE)
        if match:
            reference_content = match.group(1).strip()
            break

if reference_content is None:
    print("Aucun contenu trouvé entre </main> et </body>.")
else:
    # Ajout des balises de repère pour insertion manuelle plus tard
    custom_block = f"\n    {insertion_marker_start}\n    {reference_content}\n    {insertion_marker_end}\n"

    for file in html_files:
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Vérifier s'il contient déjà un bloc personnalisé
        if insertion_marker_start in content:
            print(f"{file} contient déjà un bloc personnalisé. Ignoré.")
            continue

        # Insérer juste avant </body>
        new_content = re.sub(r'(</body>)', custom_block + r'\n\1', content, flags=re.IGNORECASE)

        with open(file, 'w', encoding='utf-8') as f:
            f.write(new_content)
            print(f"{file} mis à jour avec le contenu personnalisé.")
