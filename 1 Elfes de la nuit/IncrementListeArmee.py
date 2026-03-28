import csv

# Nettoie les noms de fichiers (facultatif ici, mais utile si tes titres ont des caractères spéciaux)
def clean_filename(name):
    return name.replace("’", "").replace("'", "").replace(",", ",").replace(":", "").replace("  ", " ").strip()

# Fichier de sortie
output_file = "Increment_Liste_Armee.html"

# Lecture CSV et génération
with open("0 export_articles.csv", newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';')
    with open(output_file, "w", encoding="utf-8") as f_out:
        for row in reader:
            titre = clean_filename(row['Titre'].strip())
            prix = row['Prix'].strip().replace(' €', '€')
            photo1 = row['Photo 1'].strip()

            # Génération du bloc HTML
            bloc = f"""<div class="item">
  <a href="1 Elfes de la nuit/{titre}.html" target="_blank"><img src="1 Elfes de la nuit/{photo1}.jpg" alt="{titre}"></a>
  <h3>{titre}</h3>
  <p><strong>Prix : {prix}</strong></p>
</div>

"""
            f_out.write(bloc)

print(f"Fichier '{output_file}' généré avec succès.")
