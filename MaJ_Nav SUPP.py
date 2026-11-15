import os
import re

# ============================================================
# Configuration
# ============================================================
FICHIER_SOURCE  = "index.html"   # Le fichier qui contient la nav de référence
ENCODAGE        = "utf-8"        # Encodage des fichiers HTML

# Fichiers à ne PAS modifier (en plus de index.html lui-même)
EXCLUSIONS = {
    "index.html",
    "POLITIQUE_CONFIDENTIALITE.html",
}

# ============================================================
# Fonctions
# ============================================================

def extraire_nav(contenu):
    """Extrait le bloc <nav class="sidebar">...</nav> d'un fichier HTML."""
    pattern = re.compile(
        r'<nav\s+class=["\']sidebar["\'].*?</nav>',
        re.DOTALL | re.IGNORECASE
    )
    match = pattern.search(contenu)
    if match:
        return match.group(0)
    return None


def remplacer_nav(contenu, nouvelle_nav):
    """Remplace le bloc <nav class="sidebar">...</nav> existant par la nouvelle nav."""
    pattern = re.compile(
        r'<nav\s+class=["\']sidebar["\'].*?</nav>',
        re.DOTALL | re.IGNORECASE
    )
    nouveau_contenu, nb = pattern.subn(nouvelle_nav, contenu, count=1)
    return nouveau_contenu, nb


def ajouter_nav_apres_header(contenu, nouvelle_nav):
    """Si la page n'a pas de nav, l'insère juste après </header>."""
    pattern = re.compile(r'(</header>)', re.IGNORECASE)
    nouveau_contenu, nb = pattern.subn(r'\1\n\n' + nouvelle_nav, contenu, count=1)
    return nouveau_contenu, nb

# ============================================================
# Lecture de la nav source depuis index.html
# ============================================================
print(f"📖 Lecture de la nav depuis '{FICHIER_SOURCE}'...")

try:
    with open(FICHIER_SOURCE, "r", encoding=ENCODAGE) as f:
        contenu_index = f.read()
except FileNotFoundError:
    print(f"❌ Erreur : '{FICHIER_SOURCE}' introuvable. Lance le script depuis la racine de MonSiteWeb.")
    exit(1)

nav_reference = extraire_nav(contenu_index)

if not nav_reference:
    print("❌ Erreur : aucune <nav class=\"sidebar\"> trouvée dans index.html.")
    exit(1)

print(f"✅ Nav extraite ({len(nav_reference)} caractères)\n")

# ============================================================
# Scan et mise à jour de tous les fichiers HTML à la racine
# ============================================================
fichiers_html = [
    f for f in os.listdir(".")
    if f.endswith(".html") and f not in EXCLUSIONS
]

fichiers_html.sort()

modifies   = []
ignores    = []
sans_nav   = []
erreurs    = []

for nom_fichier in fichiers_html:
    try:
        with open(nom_fichier, "r", encoding=ENCODAGE) as f:
            contenu = f.read()

        # Cas 1 : la page a déjà une nav → on la remplace
        if re.search(r'<nav\s+class=["\']sidebar["\']', contenu, re.IGNORECASE):
            nouveau_contenu, nb = remplacer_nav(contenu, nav_reference)
            if nb > 0 and nouveau_contenu != contenu:
                with open(nom_fichier, "w", encoding=ENCODAGE) as f:
                    f.write(nouveau_contenu)
                print(f"  ✅ Mis à jour     : {nom_fichier}")
                modifies.append(nom_fichier)
            else:
                print(f"  ⏭️  Déjà à jour    : {nom_fichier}")
                ignores.append(nom_fichier)

        # Cas 2 : la page n'a pas de nav → on l'insère après </header>
        elif "</header>" in contenu.lower():
            nouveau_contenu, nb = ajouter_nav_apres_header(contenu, nav_reference)
            if nb > 0:
                with open(nom_fichier, "w", encoding=ENCODAGE) as f:
                    f.write(nouveau_contenu)
                print(f"  ➕ Nav ajoutée    : {nom_fichier}")
                sans_nav.append(nom_fichier)
            else:
                print(f"  ⚠️  Pas de </header> trouvé : {nom_fichier}")
                erreurs.append(nom_fichier)
        else:
            print(f"  ⚠️  Pas de repère  : {nom_fichier} (ni nav ni header)")
            erreurs.append(nom_fichier)

    except Exception as e:
        print(f"  ❌ Erreur sur {nom_fichier} : {e}")
        erreurs.append(nom_fichier)

# ============================================================
# Résumé
# ============================================================
print(f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 Résumé
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ✅ Mis à jour     : {len(modifies)} fichier(s)
  ➕ Nav ajoutée    : {len(sans_nav)} fichier(s)
  ⏭️  Déjà à jour    : {len(ignores)} fichier(s)
  ⚠️  Problèmes      : {len(erreurs)} fichier(s)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")

if erreurs:
    print("Fichiers avec problèmes :")
    for f in erreurs:
        print(f"  - {f}")
