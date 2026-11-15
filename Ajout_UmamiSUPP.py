import os
import re

# ============================================================
# Ajout du suivi Umami dans le <head> de toutes les pages HTML
# À lancer depuis la RACINE de MonSiteWeb (là où se trouve index.html)
# ============================================================

SCRIPT_SRC = "https://cloud.umami.is/script.js"

# Dossiers ignorés (le dossier .git, les morceaux de page chargés en JS...)
DOSSIERS_IGNORES = {".git", "includes", "css", "images", "node_modules"}

# Les petites pages qui affichent une seule photo (dossiers LienPhoto)
# comptent comme des "événements" Umami. Mets True pour les suivre aussi.
INCLURE_LIENPHOTO = False

# Fichiers ignorés si leur nom contient un de ces mots (sauvegardes...)
MOTS_IGNORES = ("backup", "increment_liste_armee")

# ============================================================
# Outils
# ============================================================
REGEX_ID = re.compile(r"^[0-9a-fA-F]{8}(-[0-9a-fA-F]{4}){3}-[0-9a-fA-F]{12}$")


def lire(chemin):
    """Lit un fichier en conservant son encodage et ses fins de ligne."""
    for enc in ("utf-8", "cp1252"):
        try:
            with open(chemin, "r", encoding=enc, newline="") as f:
                return f.read(), enc
        except UnicodeDecodeError:
            continue
    return None, None


def ecrire(chemin, contenu, enc):
    with open(chemin, "w", encoding=enc, newline="") as f:
        f.write(contenu)


# ============================================================
# Vérifications de départ
# ============================================================
if not os.path.exists("index.html"):
    print("❌ index.html introuvable : lance ce script depuis la racine de MonSiteWeb.")
    input("Appuie sur Entrée pour quitter...")
    raise SystemExit(1)

print("Colle ton identifiant de site Umami (Website ID), puis Entrée :")
website_id = input("> ").strip()

if not REGEX_ID.match(website_id):
    print("❌ Ce n'est pas un identifiant valide (il ressemble à xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx).")
    input("Appuie sur Entrée pour quitter...")
    raise SystemExit(1)

LIGNE_UMAMI = f'  <script defer src="{SCRIPT_SRC}" data-website-id="{website_id}"></script>\n'

# ============================================================
# Analyse (rien n'est modifié à cette étape)
# ============================================================
a_modifier, deja_ok, sans_head, illisibles = [], [], [], []

for dossier, sous_dossiers, fichiers in os.walk("."):
    sous_dossiers[:] = [
        d for d in sous_dossiers
        if d not in DOSSIERS_IGNORES and (INCLURE_LIENPHOTO or d != "LienPhoto")
    ]
    for nom in fichiers:
        if not nom.lower().endswith(".html"):
            continue
        if any(m in nom.lower() for m in MOTS_IGNORES):
            continue

        chemin = os.path.join(dossier, nom)
        contenu, enc = lire(chemin)

        if contenu is None:
            illisibles.append(chemin)
        elif SCRIPT_SRC in contenu:
            deja_ok.append(chemin)
        elif not re.search(r"</head>", contenu, re.IGNORECASE):
            sans_head.append(chemin)
        else:
            a_modifier.append((chemin, enc))

print(f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔎 Analyse terminée
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  À modifier        : {len(a_modifier)} page(s)
  Déjà équipées     : {len(deja_ok)} page(s)
  Sans </head>      : {len(sans_head)} page(s)
  Illisibles        : {len(illisibles)} page(s)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")

if not a_modifier:
    print("Rien à faire.")
    input("Appuie sur Entrée pour quitter...")
    raise SystemExit(0)

reponse = input(f"Ajouter le suivi Umami dans ces {len(a_modifier)} pages ? (o/n) : ").strip().lower()
if reponse not in ("o", "oui", "y"):
    print("Annulé, aucune page modifiée.")
    input("Appuie sur Entrée pour quitter...")
    raise SystemExit(0)

# ============================================================
# Modification : la ligne est ajoutée juste avant le premier </head>
# ============================================================
nb = 0
for chemin, enc in a_modifier:
    contenu, _ = lire(chemin)
    # On reprend le type de fin de ligne de la page (Windows = \r\n)
    fin = "\r\n" if "\r\n" in contenu else "\n"
    ligne = LIGNE_UMAMI.rstrip("\n") + fin
    nouveau = re.sub(r"</head>", lambda m: ligne + "</head>", contenu, count=1, flags=re.IGNORECASE)
    ecrire(chemin, nouveau, enc)
    nb += 1

print(f"\n✅ Terminé : {nb} page(s) modifiée(s).")

if sans_head:
    print("\n⚠️  Pages sans </head> (non modifiées) :")
    for c in sans_head:
        print("  -", c)

if illisibles:
    print("\n⚠️  Pages illisibles (non modifiées) :")
    for c in illisibles:
        print("  -", c)

input("\nAppuie sur Entrée pour quitter...")
