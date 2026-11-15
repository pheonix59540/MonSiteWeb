import os
import re

# ============================================================
# MaJ_Site.py : met à jour TOUTES les pages à partir de index.html
#
#   1. <head>   : lien vers le CSS, suivi Umami, suppression de l'ancien
#                 script qui forçait la hauteur du header
#   2. <header> : s'assure que le bandeau existe
#   3. Menu     : recopie le <nav class="sidebar"> de index.html
#                 (liens adaptés pour les pages rangées dans un sous-dossier)
#   4. Pied de page : bloc "footer-container" + chargement de includes/footer.html
#
# À lancer depuis la RACINE de MonSiteWeb (là où se trouve index.html).
# Les pages des sous-dossiers (articles) sont traitées aussi.
# ============================================================

FICHIER_SOURCE = "index.html"

# Pages à ne PAS modifier (noms de fichiers, en minuscules)
EXCLUSIONS = {
    "index.html",
    "politique_confidentialite.html",
}

# Fichiers ignorés si leur nom contient un de ces mots
MOTS_IGNORES = ("backup", "increment_liste_armee")

# Dossiers ignorés (les dossiers qui finissent par _mini le sont aussi)
DOSSIERS_IGNORES = {".git", "includes", "css", "images", "LienPhoto", "node_modules"}

# ============================================================
# Motifs de recherche
# ============================================================
RE_NAV = re.compile(
    r'<nav\b[^>]*\bclass\s*=\s*["\'][^"\']*\bsidebar\b[^"\']*["\'][^>]*>.*?</nav>',
    re.IGNORECASE | re.DOTALL)
RE_BODY = re.compile(r'<body\b[^>]*>', re.IGNORECASE)
RE_HEADER = re.compile(r'<header\b', re.IGNORECASE)
RE_FIN_HEAD = re.compile(r'</head>', re.IGNORECASE)
RE_FIN_BODY = re.compile(r'\s*</body>', re.IGNORECASE)
RE_UMAMI = re.compile(r'<script\b[^>]*cloud\.umami\.is/script\.js[^>]*>\s*</script>',
                      re.IGNORECASE | re.DOTALL)
RE_LIEN_CSS = re.compile(r'<link\b[^>]*href\s*=\s*["\'][^"\']*style\.css["\'][^>]*>', re.IGNORECASE)
RE_ANCIEN_SCRIPT_HEADER = re.compile(
    r'[ \t]*<script>\s*function adjustHeaderHeight\(\).*?</script>[ \t]*\r?\n?',
    re.IGNORECASE | re.DOTALL)
RE_SCRIPT_FOOTER = re.compile(
    r'[ \t]*<script>[^<]*?fetch\(\s*["\'][^"\']*includes/footer\.html["\']\s*\).*?</script>[ \t]*\r?\n?',
    re.IGNORECASE | re.DOTALL)
RE_DIV_FOOTER = re.compile(
    r'[ \t]*<div\s+id=["\']footer-container["\']\s*>\s*</div>[ \t]*\r?\n?', re.IGNORECASE)
RE_BLOC_PERSO = re.compile(
    r'[ \t]*<!--\s*CONTENU PERSONNALIS[ÉE]\s+D[ÉE]BUT\s*-->.*?<!--\s*CONTENU PERSONNALIS[ÉE]\s+FIN\s*-->[ \t]*\r?\n?',
    re.IGNORECASE | re.DOTALL)
RE_HREF = re.compile(r'href\s*=\s*(["\'])(.*?)\1', re.IGNORECASE | re.DOTALL)


# ============================================================
# Outils
# ============================================================
def lire(chemin):
    """Lit un fichier en gardant son encodage et ses fins de ligne."""
    for enc in ("utf-8", "cp1252"):
        try:
            with open(chemin, "r", encoding=enc, newline="") as f:
                return f.read(), enc
        except UnicodeDecodeError:
            continue
    return None, None


def vers_eol(texte, eol):
    return texte.replace("\r\n", "\n").replace("\n", eol)


def adapter_liens(nav, prefixe, est_accueil):
    """
    Adapte les liens du menu à l'endroit où se trouve la page :
      - page dans un sous-dossier : on ajoute ../ devant chaque lien
      - ancre (#figurines...)     : sur une autre page que l'accueil, elle mène à index.html#...
    """
    def remplacer(m):
        guillemet, url = m.group(1), m.group(2)
        if re.match(r'(https?:|mailto:|tel:|javascript:|//|/)', url, re.IGNORECASE):
            return m.group(0)
        if url.startswith("#"):
            nouveau = url if est_accueil else prefixe + "index.html" + url
        else:
            nouveau = prefixe + url
        return f"href={guillemet}{nouveau}{guillemet}"
    return RE_HREF.sub(remplacer, nav)


def traiter(contenu, prefixe, modele_nav, modele_footer, balise_umami):
    """Retourne (nouveau_contenu, [étapes modifiées]) ou (None, motif) en cas de problème."""
    eol = "\r\n" if "\r\n" in contenu else "\n"
    modifs = []

    if not RE_FIN_HEAD.search(contenu):
        return None, "pas de </head>"
    if not RE_BODY.search(contenu) or not re.search(r'</body>', contenu, re.IGNORECASE):
        return None, "pas de <body> ... </body>"

    # ---------- 1. <head> ----------
    avant = contenu
    contenu = RE_ANCIEN_SCRIPT_HEADER.sub("", contenu)

    lien_css = f'<link rel="stylesheet" href="{prefixe}css/style.css">'
    m = RE_LIEN_CSS.search(contenu)
    if m:
        nouveau_lien = re.sub(r'href\s*=\s*["\'][^"\']*["\']', f'href="{prefixe}css/style.css"', m.group(0), count=1)
        contenu = contenu[:m.start()] + nouveau_lien + contenu[m.end():]
    else:
        contenu = RE_FIN_HEAD.sub(lambda mm: "  " + lien_css + eol + mm.group(0), contenu, count=1)

    if balise_umami and not RE_UMAMI.search(contenu):
        contenu = RE_FIN_HEAD.sub(lambda mm: "  " + balise_umami + eol + mm.group(0), contenu, count=1)
    if contenu != avant:
        modifs.append("head")

    # ---------- 2. <header> ----------
    avant = contenu
    if not RE_HEADER.search(contenu):
        contenu = RE_BODY.sub(lambda mm: mm.group(0) + eol + "  <header></header>", contenu, count=1)
    if contenu != avant:
        modifs.append("header")

    # ---------- 3. Menu ----------
    avant = contenu
    nav = vers_eol(adapter_liens(modele_nav, prefixe, False), eol)
    if RE_NAV.search(contenu):
        contenu = RE_NAV.sub(lambda mm: nav, contenu, count=1)
    else:
        contenu = re.sub(r'</header>', lambda mm: mm.group(0) + eol + eol + "  " + nav,
                         contenu, count=1, flags=re.IGNORECASE)
    if contenu != avant:
        modifs.append("menu")

    # ---------- 4. Pied de page ----------
    avant = contenu
    contenu = RE_BLOC_PERSO.sub("", contenu)
    contenu = RE_SCRIPT_FOOTER.sub("", contenu)
    contenu = RE_DIV_FOOTER.sub("", contenu)
    script = vers_eol(modele_footer.replace("includes/footer.html", prefixe + "includes/footer.html"), eol)
    bloc = ("  <div id=\"footer-container\"></div>" + eol + eol + "  " + script)
    # on remet le bloc juste avant le DERNIER </body>
    dernier = list(RE_FIN_BODY.finditer(contenu))[-1]
    contenu = contenu[:dernier.start()] + eol + eol + bloc + eol + eol + "</body>" + contenu[dernier.end():]
    if contenu != avant:
        modifs.append("pied de page")

    return contenu, modifs


# ============================================================
# Lecture du modèle : index.html
# ============================================================
if not os.path.exists(FICHIER_SOURCE):
    print(f"❌ '{FICHIER_SOURCE}' introuvable : lance ce script depuis la racine de MonSiteWeb.")
    input("Appuie sur Entrée pour quitter...")
    raise SystemExit(1)

index, _ = lire(FICHIER_SOURCE)
m_nav = RE_NAV.search(index)
m_footer = RE_SCRIPT_FOOTER.search(index)
m_umami = RE_UMAMI.search(index)

if not m_nav:
    print('❌ Aucune <nav class="sidebar"> trouvée dans index.html.')
    input("Appuie sur Entrée pour quitter...")
    raise SystemExit(1)
if not m_footer:
    print('❌ Le script de chargement du pied de page (includes/footer.html) est introuvable dans index.html.')
    input("Appuie sur Entrée pour quitter...")
    raise SystemExit(1)

modele_nav = m_nav.group(0)
modele_footer = m_footer.group(0).strip()
balise_umami = m_umami.group(0).strip() if m_umami else None

print("📖 Modèle lu dans index.html :")
print(f"   - menu       : {modele_nav.count('<a ')} liens")
print(f"   - pied de page : chargement de includes/footer.html")
print(f"   - suivi Umami  : {'oui' if balise_umami else 'non (absent de index.html)'}\n")

# ============================================================
# Analyse (rien n'est modifié à cette étape)
# ============================================================
a_ecrire, a_jour, problemes = [], [], []

for dossier, sous_dossiers, fichiers in os.walk("."):
    sous_dossiers[:] = sorted(
        d for d in sous_dossiers
        if d not in DOSSIERS_IGNORES and not d.endswith("_mini"))
    rel = os.path.relpath(dossier, ".")
    profondeur = 0 if rel == "." else len(rel.replace("\\", "/").split("/"))
    prefixe = "../" * profondeur

    for nom in sorted(fichiers):
        bas = nom.lower()
        if not bas.endswith(".html") or bas == ".html":
            continue
        if bas in EXCLUSIONS and profondeur == 0:
            continue
        if any(mot in bas for mot in MOTS_IGNORES):
            continue

        chemin = os.path.normpath(os.path.join(dossier, nom))
        contenu, enc = lire(chemin)
        if contenu is None:
            problemes.append((chemin, "encodage illisible"))
            continue

        nouveau, resultat = traiter(contenu, prefixe, modele_nav, modele_footer, balise_umami)
        if nouveau is None:
            problemes.append((chemin, resultat))
            continue
        try:
            nouveau.encode(enc)
        except UnicodeEncodeError:
            problemes.append((chemin, "caractère impossible à enregistrer dans cet encodage"))
            continue

        if nouveau == contenu:
            a_jour.append(chemin)
        else:
            a_ecrire.append((chemin, enc, nouveau, resultat))

compte = {}
for _, _, _, etapes in a_ecrire:
    for e in etapes:
        compte[e] = compte.get(e, 0) + 1

print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
print("🔎 Analyse terminée")
print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
print(f"  À modifier       : {len(a_ecrire)} page(s)")
for etape in ("head", "header", "menu", "pied de page"):
    if etape in compte:
        print(f"      dont {etape:<13}: {compte[etape]}")
print(f"  Déjà à jour      : {len(a_jour)} page(s)")
print(f"  Problèmes        : {len(problemes)} page(s)")
print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

if a_ecrire:
    print("\nExemples de pages qui vont changer :")
    for chemin, _, _, etapes in a_ecrire[:12]:
        print(f"  - {chemin}   ({', '.join(etapes)})")
    if len(a_ecrire) > 12:
        print(f"  ... et {len(a_ecrire) - 12} autre(s)")

if problemes:
    print("\n⚠️  Pages ignorées (à regarder à la main) :")
    for chemin, motif in problemes:
        print(f"  - {chemin} : {motif}")

if not a_ecrire:
    print("\nRien à modifier.")
    input("\nAppuie sur Entrée pour quitter...")
    raise SystemExit(0)

reponse = input(f"\nMettre à jour ces {len(a_ecrire)} page(s) ? (o/n) : ").strip().lower()
if reponse not in ("o", "oui", "y"):
    print("Annulé, aucune page modifiée.")
    input("Appuie sur Entrée pour quitter...")
    raise SystemExit(0)

# ============================================================
# Écriture
# ============================================================
for chemin, enc, nouveau, _ in a_ecrire:
    with open(chemin, "w", encoding=enc, newline="") as f:
        f.write(nouveau)

print(f"\n✅ Terminé : {len(a_ecrire)} page(s) mise(s) à jour.")
print("Conseil : regarde 'git status', teste en local, puis git add / commit / push.")
input("\nAppuie sur Entrée pour quitter...")
