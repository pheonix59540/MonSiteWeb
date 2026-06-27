import csv
import os

# ============================================================
# Configuration — adapte ces deux valeurs si besoin
# ============================================================
FICHIER_CSV    = "0_export_articles.csv"
FICHIER_SORTIE = "0 liste_articles.txt"
SEPARATEUR_CSV = ";"   # Change en ";" si ton CSV utilise des points-virgules

# Dossier contenant les pages HTML générées (relatif à la racine du site)
# Exemple : "4 Plateaux de mouvement carré"
# Le script le détecte automatiquement depuis le dossier courant
DOSSIER = os.path.basename(os.getcwd())

# ============================================================
# Génération
# ============================================================
lignes_generees = 0

with open(FICHIER_CSV, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=SEPARATEUR_CSV)

    with open(FICHIER_SORTIE, "w", encoding="utf-8") as sortie:

        for ligne in reader:
            titre = ligne.get('titre', '').strip()
            prix  = ligne.get('prix', '').strip()
            photo = ligne.get('Photo 1', '').strip()

            if not titre:  # ignore les lignes vides
                continue

            bloc = f"""<div class="item">
  <a href="{DOSSIER}/{titre}.html" target="_blank"><img src="{DOSSIER}/{photo}.jpg" alt="{titre}"></a>
  <h3>{titre}</h3>
  <p><strong>Prix : {prix}</strong></p>
</div>
"""
            sortie.write(bloc)
            lignes_generees += 1
            print(f"Bloc généré : {titre}")

print(f"\n✅ Terminé — {lignes_generees} blocs écrits dans '{FICHIER_SORTIE}'")
