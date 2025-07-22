import os
from bs4 import BeautifulSoup

root_dir = '.'  # dossier racine
index_path = os.path.join(root_dir, 'index.html')

# 1. Lire index.html
with open(index_path, 'r', encoding='utf-8') as f:
    index_html = f.read()

soup_index = BeautifulSoup(index_html, 'html.parser')

# 2. Supprimer la balise <main> de index.html
main_index = soup_index.find('main')
if main_index:
    main_index.extract()
else:
    print("⚠️ Pas de <main> dans index.html.")

# Le contenu nettoyé sans <main>
clean_index_html = soup_index

# 3. Extraire les fichiers listés dans <nav class="sidebar">
nav_sidebar = BeautifulSoup(index_html, 'html.parser').find('nav', class_='sidebar')
if not nav_sidebar:
    print("❌ Erreur : pas de <nav class='sidebar'> dans index.html")
    exit(1)

links = nav_sidebar.find_all('a')
files_to_update = [link.get('href') for link in links if link.get('href')]

# 4. Pour chaque page cible
for filename in files_to_update:
    filepath = os.path.join(root_dir, filename)
    if not os.path.isfile(filepath):
        print(f"❌ Fichier {filename} non trouvé.")
        continue

    print(f"✅ Traitement de {filename} ...")
    with open(filepath, 'r', encoding='utf-8') as f:
        target_html = f.read()

    soup_target = BeautifulSoup(target_html, 'html.parser')

    # Extraire le <main> original de la page cible
    main_target = soup_target.find('main')
    if not main_target:
        print(f"⚠️ Pas de <main> dans {filename}, on saute.")
        continue

    # Créer une copie du HTML d'index sans <main>
    soup_copy = BeautifulSoup(str(clean_index_html), 'html.parser')

    # Ajouter <main> et <div id="footer-container"></div> à la fin du <body>
    body = soup_copy.body
    if body:
        body.append(main_target)  # on garde le <main> original
        body.append(soup_target.new_tag("div", id="footer-container"))
    else:
        print(f"⚠️ Pas de <body> dans {filename}, insertion impossible.")
        continue

    # Sauvegarder la page modifiée
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(str(soup_copy))

print("🎉 Terminé.")
