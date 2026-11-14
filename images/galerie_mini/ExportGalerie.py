import os

# Extensions autorisées
extensions = (".jpg", ".jpeg", ".png")

# Dossier de destination
dossier_lienphoto = "LienPhoto"
os.makedirs(dossier_lienphoto, exist_ok=True)

# Liste des blocs HTML pour l'index
blocs_html = []

# Parcours des fichiers à la racine
for fichier in os.listdir("."):
    if fichier.lower().endswith(extensions) and os.path.isfile(fichier):
        nom, ext = os.path.splitext(fichier)
        ext = ext.lower()

        # Création du fichier HTML dans LienPhoto/
        chemin_html = os.path.join(dossier_lienphoto, f"{nom}.html")
        with open(chemin_html, "w", encoding="utf-8") as f:
            f.write(f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>{nom}</title>
    <style>
        body {{ margin: 0; background-color: #111; display: flex; justify-content: center; align-items: center; height: 100vh; }}
        img {{ max-width: 100%; max-height: 100vh; object-fit: contain; }}
    </style>
</head>
<body>
    <img src="../{nom}{ext}" alt="Galerie">
</body>
</html>""")

        # Ajout du bloc HTML pour l'index
        bloc = f"""<div class="item">
    <a href="5 Galerie/LienPhoto/{nom}.html" target="_blank"><img src="5 Galerie/{nom}{ext}" alt="Galerie"></a>
</div>"""
        blocs_html.append(bloc)

# Écriture de l'index HTML à la racine
with open("index.html", "w", encoding="utf-8") as index:
    index.write("<!DOCTYPE html>\n<html lang='fr'>\n<head><meta charset='UTF-8'><title>Galerie</title></head>\n<body>\n")
    index.write("\n".join(blocs_html))
    index.write("\n</body>\n</html>")

print("✔️ Script terminé : pages HTML générées pour chaque image + index.html")
