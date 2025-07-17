
import os
import re

# Définir le nom du fichier modèle (contenant la nav à copier)
fichier_modele = "index.html"

# Lire le contenu de la nav dans index.html
with open(fichier_modele, "r", encoding="utf-8") as f:
    contenu = f.read()

# Extraire le bloc <nav class="sidebar"> ... </nav>
pattern_nav = re.compile(r'<nav class="sidebar">.*?</nav>', re.DOTALL)
nav_match = pattern_nav.search(contenu)

if not nav_match:
    print("❌ Impossible de trouver le bloc <nav class=\"sidebar\"> dans index.html")
    exit()

nouvelle_nav = nav_match.group(0)

# Liste tous les fichiers HTML sauf index.html
for fichier in os.listdir():
    if fichier.endswith(".html") and fichier != fichier_modele:
        with open(fichier, "r", encoding="utf-8") as f:
            contenu_page = f.read()

        if pattern_nav.search(contenu_page):
            contenu_modifie = pattern_nav.sub(nouvelle_nav, contenu_page)

            with open(fichier, "w", encoding="utf-8") as f:
                f.write(contenu_modifie)

            print(f"✅ Bloc <nav> remplacé dans : {fichier}")
        else:
            print(f"⚠️ Pas de bloc <nav class=\"sidebar\"> trouvé dans : {fichier}")

