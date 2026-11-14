import os
import re
import csv
import html
import unicodedata

# ============================================================
# Mise à jour des sliders de l'accueil
#
#  1. Lit les photos des dossiers  figurines_mini, decors_mini,
#     accessoires_mini, galerie_mini
#  2. Tient à jour le fichier "0 carrousels.csv"  (categorie;photo;lien)
#  3. Génère  includes/carousel_figurines.html, carousel_decors.html...
#
# À lancer depuis la RACINE de MonSiteWeb (là où se trouve index.html)
# ============================================================

FICHIER_CSV = "0 carrousels.csv"

# nom dans le CSV : (dossier des photos, fichier généré)
CATEGORIES = {
    "figurines":   ("figurines_mini",   "includes/carousel_figurines.html"),
    "decors":      ("decors_mini",      "includes/carousel_decors.html"),
    "accessoires": ("accessoires_mini", "includes/carousel_accessoires.html"),
    "galerie":     ("galerie_mini",     "includes/carousel_galerie.html"),
}

EXTENSIONS_PHOTOS = (".jpg", ".jpeg", ".png", ".webp", ".gif")

# Dossiers ignorés quand on cherche les pages pour proposer un lien automatique
DOSSIERS_IGNORES = {".git", "includes", "css", "images", "LienPhoto", "node_modules"}


# ============================================================
# Outils
# ============================================================
def normaliser(texte):
    return unicodedata.normalize("NFC", texte).casefold()


def tri_naturel(nom):
    """Tri 'Photo 2' avant 'Photo 10'."""
    return [int(t) if t.isdigit() else t.casefold() for t in re.split(r"(\d+)", nom)]


def trouver_dossier_photos(nom_dossier):
    """Cherche le dossier à la racine, puis dans images/. Retourne son chemin relatif ou None."""
    for candidat in (nom_dossier, "images/" + nom_dossier):
        if os.path.isdir(candidat):
            return candidat
    return None


def verifier_lien(lien):
    """
    Vérifie que la page existe avec EXACTEMENT la même casse (GitHub est sensible aux majuscules).
    Retourne (ok, message).
    """
    chemin = lien.split("#")[0].split("?")[0].strip()
    if chemin.startswith("./"):
        chemin = chemin[2:]
    if not chemin or chemin.startswith(("http://", "https://")):
        return True, ""

    courant = "."
    corrige = []
    casse_differente = False
    for morceau in [m for m in chemin.replace("\\", "/").split("/") if m]:
        try:
            noms = os.listdir(courant)
        except OSError:
            return False, "page introuvable"
        if morceau in noms:
            corrige.append(morceau)
        else:
            alternatives = [n for n in noms if normaliser(n) == normaliser(morceau)]
            if not alternatives:
                return False, "page introuvable"
            morceau = alternatives[0]
            corrige.append(morceau)
            casse_differente = True
        courant = os.path.join(courant, morceau)

    if casse_differente:
        return False, "majuscules/accents différents, le vrai nom est : " + "/".join(corrige)
    return True, ""


def indexer_pages():
    """Liste les pages HTML du site : nom sans extension -> chemins possibles."""
    index = {}
    for dossier, sous_dossiers, fichiers in os.walk("."):
        sous_dossiers[:] = [
            d for d in sous_dossiers
            if d not in DOSSIERS_IGNORES and not d.endswith("_mini")
        ]
        for nom in fichiers:
            if nom.lower().endswith(".html"):
                chemin = os.path.relpath(os.path.join(dossier, nom), ".").replace("\\", "/")
                index.setdefault(normaliser(os.path.splitext(nom)[0]), []).append(chemin)
    return index


def proposer_lien(photo, index_pages):
    """Si la photo s'appelle comme une page (ex. 'Chests D20 1.jpg' -> 'Chests D20.html'), on la propose."""
    nom = os.path.splitext(photo)[0]
    candidats = []
    for c in (nom, re.sub(r"[\s_-]*\d+$", "", nom)):
        c = re.sub(r"[\s_-]*mini$", "", c, flags=re.IGNORECASE).strip()
        if c and c not in candidats:
            candidats.append(c)
    for c in candidats:
        trouves = index_pages.get(normaliser(c), [])
        if len(trouves) == 1:       # on ne propose que si c'est sans ambiguïté
            return trouves[0]
    return ""


def lire_csv():
    """Lit le CSV (UTF-8 ou Windows, séparateur ; , ou tabulation)."""
    if not os.path.exists(FICHIER_CSV):
        return []
    texte = None
    for enc in ("utf-8-sig", "cp1252"):
        try:
            with open(FICHIER_CSV, "r", encoding=enc, newline="") as f:
                texte = f.read()
            break
        except UnicodeDecodeError:
            continue
    if texte is None:
        return []

    lignes = texte.splitlines()
    if not lignes:
        return []
    entete = lignes[0]
    sep = ";" if ";" in entete else ("\t" if "\t" in entete else ",")

    lecteur = csv.reader(lignes, delimiter=sep)
    colonnes = [normaliser(c).strip() for c in next(lecteur, [])]
    colonnes = [c.replace("é", "e") for c in colonnes]
    try:
        i_cat, i_photo, i_lien = colonnes.index("categorie"), colonnes.index("photo"), colonnes.index("lien")
    except ValueError:
        print("❌ Le CSV doit avoir les colonnes : categorie ; photo ; lien")
        input("Appuie sur Entrée pour quitter...")
        raise SystemExit(1)

    rows = []
    for r in lecteur:
        if len(r) <= i_photo or not r[i_photo].strip():
            continue
        rows.append({
            "categorie": normaliser(r[i_cat]).replace("é", "e").strip() if len(r) > i_cat else "",
            "photo": r[i_photo].strip(),
            "lien": r[i_lien].strip() if len(r) > i_lien else "",
        })
    return rows


def ecrire_csv(rows):
    with open(FICHIER_CSV, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(["categorie", "photo", "lien"])
        for r in rows:
            w.writerow([r["categorie"], r["photo"], r["lien"]])


# ============================================================
# Programme principal
# ============================================================
if not os.path.exists("index.html"):
    print("❌ index.html introuvable : lance ce script depuis la racine de MonSiteWeb.")
    input("Appuie sur Entrée pour quitter...")
    raise SystemExit(1)

rows = lire_csv()
index_pages = indexer_pages()
nouvelles, absentes, avertissements, sans_lien = [], [], [], []

for cat, (nom_dossier, _) in CATEGORIES.items():
    dossier = trouver_dossier_photos(nom_dossier)
    if dossier is None:
        print(f"⚠️  Dossier '{nom_dossier}' introuvable (ni à la racine, ni dans images/) : catégorie '{cat}' ignorée.")
        continue

    sur_disque = sorted(
        [n for n in os.listdir(dossier) if n.lower().endswith(EXTENSIONS_PHOTOS)],
        key=tri_naturel,
    )
    deja = {r["photo"] for r in rows if r["categorie"] == cat}

    for photo in sur_disque:
        if photo not in deja:
            lien = proposer_lien(photo, index_pages)
            rows.append({"categorie": cat, "photo": photo, "lien": lien})
            nouvelles.append((cat, photo, lien))

# Mise à jour du CSV (les anciennes lignes et leur ordre sont conservés)
ecrire_csv(rows)

# Génération des fichiers includes
os.makedirs("includes", exist_ok=True)
total = {}
for cat, (nom_dossier, fichier_inclus) in CATEGORIES.items():
    dossier = trouver_dossier_photos(nom_dossier)
    if dossier is None:
        continue

    morceaux = ["<!-- Fichier généré par Maj_Carrousels.py : ne pas modifier à la main -->"]
    nb = 0
    for r in [x for x in rows if x["categorie"] == cat]:
        if not os.path.isfile(os.path.join(dossier, r["photo"])):
            absentes.append((cat, r["photo"]))
            continue

        src = html.escape(f"{dossier}/{r['photo']}", quote=True)
        alt = html.escape(os.path.splitext(r["photo"])[0], quote=True)
        balise = f'<img src="{src}" alt="{alt}">'

        if not r["lien"]:
            sans_lien.append((cat, r["photo"]))
        else:
            ok, message = verifier_lien(r["lien"])
            if not ok:
                avertissements.append((cat, r["photo"], r["lien"], message))
            balise = f'<a href="{html.escape(r["lien"], quote=True)}">{balise}</a>'
        morceaux.append(balise)
        nb += 1

    with open(fichier_inclus, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(morceaux) + "\n")
    total[cat] = nb

# ============================================================
# Compte rendu
# ============================================================
print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
print("🎞️  Sliders mis à jour")
print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
for cat, nb in total.items():
    print(f"  {cat:<12}: {nb} photo(s)  ->  {CATEGORIES[cat][1]}")

if nouvelles:
    print(f"\n🆕 {len(nouvelles)} nouvelle(s) photo(s) ajoutée(s) à la fin de '{FICHIER_CSV}' :")
    for cat, photo, lien in nouvelles:
        print(f"  - [{cat}] {photo}  ->  " + (lien if lien else "(lien à remplir dans le CSV)"))

if sans_lien:
    print(f"\nℹ️  {len(sans_lien)} photo(s) sans lien (elles s'afficheront mais ne seront pas cliquables).")

if avertissements:
    print("\n⚠️  Liens à corriger dans le CSV :")
    for cat, photo, lien, message in avertissements:
        print(f"  - [{cat}] {photo} : '{lien}' -> {message}")

if absentes:
    print("\n⚠️  Lignes du CSV dont la photo n'existe plus (ignorées, tu peux les supprimer) :")
    for cat, photo in absentes:
        print(f"  - [{cat}] {photo}")

print("\nÉtape suivante : git add . / git commit / git push")
input("\nAppuie sur Entrée pour quitter...")
