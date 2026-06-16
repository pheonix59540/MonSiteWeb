import os
import csv
import qrcode
import io
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader

# ============================================================
# Configuration
# ============================================================
FICHIER_CSV     = "0 export_articles.csv"
FICHIER_PDF     = "etiquettes_qr.pdf"
SEPARATEUR_CSV  = ";"
ENCODAGE        = "cp1252"

# URL de base de ton site — chaque article sera à BASE_URL + nom_fichier
BASE_URL = "https://pheonix59540.github.io/MonSiteWeb/"

# Dossier courant — le script détecte automatiquement le sous-dossier
# ex: "1 Elfes de la Nuit" → URL = BASE_URL + "1 Elfes de la Nuit/Titre.html"
SOUS_DOSSIER = os.path.basename(os.getcwd())

# ============================================================
# Mise en page A4 — 4 colonnes x 5 lignes = 20 étiquettes
# ============================================================
PAGE_W, PAGE_H = A4          # 595 x 842 points

COLS        = 4
ROWS        = 5
MARGE       = 8 * mm         # marge extérieure
ESPACEMENT  = 4 * mm         # espace entre étiquettes

# Taille d'une étiquette
ETQ_W = (PAGE_W - 2 * MARGE - (COLS - 1) * ESPACEMENT) / COLS
ETQ_H = (PAGE_H - 2 * MARGE - (ROWS - 1) * ESPACEMENT) / ROWS

QR_SIZE     = ETQ_W * 0.60   # QR code = 60% de la largeur
FONT_TITRE  = 6.5
FONT_PRIX   = 8
PADDING     = 3 * mm

# ============================================================
# Fonction : générer un QR code en mémoire (bytes PNG)
# ============================================================
def make_qr_bytes(url):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=8,
        border=2,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf

# ============================================================
# Fonction : dessiner une étiquette
# ============================================================
def draw_etiquette(c, x, y, titre, prix, url):
    """
    x, y = coin bas-gauche de l'étiquette (en points ReportLab)
    """
    w = ETQ_W
    h = ETQ_H

    # Fond blanc avec bordure fine
    c.setStrokeColor(colors.HexColor("#0ABAB5"))
    c.setFillColor(colors.white)
    c.roundRect(x, y, w, h, 3 * mm, fill=1, stroke=1)

    # --- QR code centré en haut ---
    qr_buf = make_qr_bytes(url)
    qr_img = ImageReader(qr_buf)
    qr_x = x + (w - QR_SIZE) / 2
    qr_y = y + h - QR_SIZE - PADDING
    c.drawImage(qr_img, qr_x, qr_y, width=QR_SIZE, height=QR_SIZE,
                preserveAspectRatio=True, mask='auto')

    # --- Nom de l'article ---
    c.setFillColor(colors.HexColor("#222222"))
    c.setFont("Helvetica-Bold", FONT_TITRE)

    # Tronque le titre si trop long
    max_chars = int(w / (FONT_TITRE * 0.55))
    titre_affiche = titre if len(titre) <= max_chars else titre[:max_chars - 2] + "…"

    titre_y = qr_y - PADDING - FONT_TITRE
    c.drawCentredString(x + w / 2, titre_y, titre_affiche)

    # --- Prix ---
    c.setFont("Helvetica-Bold", FONT_PRIX)
    c.setFillColor(colors.HexColor("#2F4F4F"))
    prix_y = titre_y - FONT_PRIX - 2
    c.drawCentredString(x + w / 2, prix_y, prix)

# ============================================================
# Lecture CSV et génération PDF
# ============================================================
articles = []

with open(FICHIER_CSV, newline='', encoding=ENCODAGE) as csvfile:
    reader = csv.DictReader(csvfile, delimiter=SEPARATEUR_CSV)
    for row in reader:
        titre = row.get('Titre', '').strip()
        prix  = row.get('Prix', '').strip()
        if not titre:
            continue

        # Construction de l'URL de la page article
        # clean_filename reproduit la logique du script de génération
        nom_fichier = (titre
            .replace("'", "")
            .replace("'", "")
            .replace("é", "e")
            .replace("à", "a"))
        url = f"{BASE_URL}{SOUS_DOSSIER}/{nom_fichier}.html"

        articles.append((titre, prix, url))

if not articles:
    print("❌ Aucun article trouvé dans le CSV. Vérifie le séparateur et l'encodage.")
    exit(1)

print(f"📦 {len(articles)} article(s) trouvé(s) — génération du PDF...")

# ============================================================
# Création du PDF
# ============================================================
c = canvas.Canvas(FICHIER_PDF, pagesize=A4)
c.setTitle("Étiquettes QR - Infinity3D")

total = len(articles)
idx   = 0

while idx < total:
    # Nouvelle page
    for row in range(ROWS):
        for col in range(COLS):
            if idx >= total:
                break

            titre, prix, url = articles[idx]

            # Coin bas-gauche de l'étiquette
            x = MARGE + col * (ETQ_W + ESPACEMENT)
            # ReportLab : y=0 en bas, on part du haut
            y = PAGE_H - MARGE - (row + 1) * ETQ_H - row * ESPACEMENT

            draw_etiquette(c, x, y, titre, prix, url)
            idx += 1

    if idx < total:
        c.showPage()  # page suivante si besoin

c.save()
print(f"✅ PDF généré : {FICHIER_PDF} ({idx} étiquettes sur {(idx // 20) + 1} page(s))")
