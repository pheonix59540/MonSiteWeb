import os
import csv

# Dossier de sortie
output_dir = "LienPhoto"
os.makedirs(output_dir, exist_ok=True)

def create_photo_link_file(photo_name):
    nom_fichier = os.path.join(output_dir, f"{photo_name}.html")
    with open(nom_fichier, "w", encoding="utf-8") as f:
        f.write(f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title></title>
    <style>
        body {{
            margin: 0;
            background-color: #000;
            display: flex;
            align-items: center;
            justify-content: center;
            height: 100vh;
        }}
        img {{
            max-width: 100%;
            max-height: 100%;
        }}
    </style>
</head>
<body>
    <img src="../{photo_name}.jpg" alt="">
</body>
</html>
""")
    print(f"Fichier image simple généré : {nom_fichier}")

# Lecture du fichier CSV
with open("0 export_articles.csv", newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';')
    for row in reader:
        for i in range(1, 7):
            photo = row.get(f"Photo {i}", "").strip()
            if photo:
                create_photo_link_file(photo)

