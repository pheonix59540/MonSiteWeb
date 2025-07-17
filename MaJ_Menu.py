import os
import re

# Définir le nom du fichier modèle
fichier_modele = "index.html"

# Lire le contenu de la nav dans index.html
with open(fichier_modele, "r", encoding="utf-8") as f:
    contenu = f.read()

# Extraire le bloc <nav class="sidebar"> ... </nav>
pattern_nav = re.compile(r'<nav class="sidebar">.*?</nav>', re.DOTALL)
nav_match = pattern_nav.search(contenu)

if not nav_match:
    print("❌ Impossible de trouver le bloc <nav class=\"sidebar\"> dans index.html")
    exit()

nouvelle_nav = nav_match.group(0)

# Bloc de script à ajouter avant </body>
footer_script = '''
<div id="footer-container"></div>
<script>
  fetch("includes/footer.html")
    .then(response => response.text())
    .then(data => {
      document.getElementById("footer-container").innerHTML = data;
    })
    .catch(error => console.error("Erreur lors du chargement du pied de page :", error));
</script>
'''

# Liste tous les fichiers HTML sauf index.html
for fichier in os.listdir():
    if fichier.endswith(".html") and fichier != fichier_modele:
        with open(fichier, "r", encoding="utf-8") as f:
            contenu_page = f.read()

        modifie = False

        # Remplacer la nav si elle existe
        if pattern_nav.search(contenu_page):
            contenu_page = pattern_nav.sub(nouvelle_nav, contenu_page)
            print(f"✅ Bloc <nav> remplacé dans : {fichier}")
            modifie = True
        else:
            print(f"⚠️ Pas de bloc <nav class=\"sidebar\"> trouvé dans : {fichier}")

        # Ajouter le bloc footer juste avant </body>
        if "</body>" in contenu_page:
            if "fetch(\"includes/footer.html\")" not in contenu_page:
                contenu_page = contenu_page.replace("</body>", f"{footer_script}\n</body>")
                print(f"➕ Pied de page ajouté dans : {fichier}")
                modifie = True
            else:
                print(f"ℹ️ Pied de page déjà présent dans : {fichier}")
        else:
            print(f"❌ Pas de balise </body> trouvée dans : {fichier}")

        # Écrire le fichier modifié si quelque chose a changé
        if modifie:
            with open(fichier, "w", encoding="utf-8") as f:
                f.write(contenu_page)
