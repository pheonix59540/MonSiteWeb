import os
import re
from bs4 import BeautifulSoup
from odf.opendocument import OpenDocumentSpreadsheet
from odf.table import Table, TableRow, TableCell
from odf.text import P

# Fonction pour créer une cellule ODS
def create_cell(text):
    cell = TableCell()
    cell.addElement(P(text=text))
    return cell

# Fonction pour extraire une taille carré type "25x25 mm"
def extract_square_size(text):
    match = re.search(r'\b(\d{1,3}x\d{1,3})\s*mm\b', text)
    return match.group(1) + " mm" if match else ""

# Fonction pour extraire une taille ronde type "32 mm"
def extract_round_size(text):
    matches = re.findall(r'\b(\d{1,3})\s*mm\b', text)
    filtered = [m for m in matches if "x" not in m]
    return filtered[0] + " mm" if filtered else ""

# Créer le document ODS
spreadsheet = OpenDocumentSpreadsheet()
table = Table(name="Articles")

# Entêtes
headers = ["Titre", "Prix", "Socle carré", "Socle rond", "Photo 1", "Photo 2", "Photo 3", "Photo 4", "Photo 5", "Photo 6"]
row = TableRow()
for h in headers:
    row.addElement(create_cell(h))
table.addElement(row)

# Traitement de chaque fichier HTML dans le dossier courant
for filename in os.listdir("."):
    if filename.endswith(".html"):
        with open(filename, "r", encoding="utf-8") as file:
            soup = BeautifulSoup(file, "lxml")

            # Titre
            titre = soup.find("h1").text.strip() if soup.find("h1") else ""

            # Prix
            prix = ""
            for p in soup.find_all("p"):
                if "prix" in p.get_text().lower():
                    match = re.search(r"(\d+[,.]?\d*) ?€", p.get_text())
                    if match:
                        prix = match.group(1) + " €"
                    break

            # Recherche de description contenant les dimensions de socle
            description_text = ""
            for p in soup.find_all("p"):
                txt = p.get_text()
                if "mm" in txt.lower():
                    description_text = txt
                    break

            socle_carre = extract_square_size(description_text)
            socle_rond = extract_round_size(description_text)

            # Images
            images = soup.select("div.gallery-details img")
            noms_images = [img["src"].rsplit(".", 1)[0] for img in images]

            # Création de la ligne
            data = [titre, prix, socle_carre, socle_rond] + noms_images
            row = TableRow()
            for cell in data:
                row.addElement(create_cell(cell))
            for _ in range(10 - len(data)):
                row.addElement(create_cell(""))

            table.addElement(row)

# Sauvegarde
spreadsheet.spreadsheet.addElement(table)
spreadsheet.save("0 export_articles.ods")
print("✅ Fichier '0 export_articles.ods' généré avec succès !")

# Garder la fenêtre ouverte
input("Appuyez sur Entrée pour quitter...")

