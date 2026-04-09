import os
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
URL_SITE    = "https://pheonix59540.github.io/MonSiteWeb/"
FICHIER_PDF = "QR_Infinity3D_Stand.pdf"
SOUS_TITRE  = "Scannez pour découvrir notre catalogue !"
LOGO_PATH   = "images/1LogoAcceuil.png"

# ============================================================
# Génération du QR code
# ============================================================
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=20,
    border=3,
)
qr.add_data(URL_SITE)
qr.make(fit=True)
img = qr.make_image(fill_color="black", back_color="white")

buf = io.BytesIO()
img.save(buf, format="PNG")
buf.seek(0)
qr_img = ImageReader(buf)

# ============================================================
# Création du PDF A4
# ============================================================
PAGE_W, PAGE_H = A4
c = canvas.Canvas(FICHIER_PDF, pagesize=A4)
c.setTitle("QR Code Stand - Infinity3D")

# Logo et QR de même taille, l'un au dessus de l'autre
ITEM_SIZE   = 120 * mm
ESPACEMENT  = 5 * mm    # espace entre logo et QR
PADDING     = 10 * mm   # marge intérieure du liseré

# Dimensions du liseré : largeur = item + marges, hauteur = logo + QR + espace + marges
LISERE_W    = ITEM_SIZE + PADDING * 2
LISERE_H    = ITEM_SIZE * 2 + ESPACEMENT + PADDING * 2

# Position du liseré centré sur la page
LISERE_X    = (PAGE_W - LISERE_W) / 2
LISERE_Y    = (PAGE_H - LISERE_H) / 2 + 10 * mm

# Fond blanc
c.setFillColor(colors.white)
c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)

# Liseré teal
c.setStrokeColor(colors.HexColor("#0ABAB5"))
c.setFillColor(colors.white)
c.setLineWidth(4)
c.roundRect(LISERE_X, LISERE_Y, LISERE_W, LISERE_H, 10*mm, fill=1, stroke=1)

# Position QR code en bas du liseré
qr_x = LISERE_X + PADDING
qr_y = LISERE_Y + PADDING

# Position logo au dessus du QR
logo_x = LISERE_X + PADDING
logo_y = qr_y + ITEM_SIZE + ESPACEMENT

# Logo
if os.path.exists(LOGO_PATH):
    logo_reader = ImageReader(LOGO_PATH)
    c.drawImage(logo_reader, logo_x, logo_y,
                width=ITEM_SIZE, height=ITEM_SIZE,
                preserveAspectRatio=True, anchor='c', mask='auto')
    print(f"✅ Logo chargé : {LOGO_PATH}")
else:
    print(f"⚠️  Logo non trouvé : {LOGO_PATH}")
    c.setFont("Helvetica-Bold", 24)
    c.setFillColor(colors.HexColor("#2F4F4F"))
    c.drawCentredString(LISERE_X + LISERE_W/2, logo_y + ITEM_SIZE/2, "Infinity3D")

# QR code
c.drawImage(qr_img, qr_x, qr_y, width=ITEM_SIZE, height=ITEM_SIZE,
            preserveAspectRatio=True, mask='auto')

# Sous-titre
c.setFont("Helvetica", 15)
c.setFillColor(colors.HexColor("#444444"))
c.drawCentredString(PAGE_W/2, LISERE_Y - 12*mm, SOUS_TITRE)

# URL
c.setFont("Helvetica", 9)
c.setFillColor(colors.HexColor("#999999"))
c.drawCentredString(PAGE_W/2, LISERE_Y - 19*mm, URL_SITE)

c.save()
print(f"✅ PDF généré : {FICHIER_PDF}")
print(f"   → Pointe vers : {URL_SITE}")
