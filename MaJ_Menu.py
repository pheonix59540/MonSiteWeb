import os
from bs4 import BeautifulSoup

# Répertoire courant
root_dir = '.'

# Tous les fichiers .html à la racine
html_files = [f for f in os.listdir(root_dir) if f.endswith('.html') and os.path.isfile(f)]

for filename in html_files:
    with open(filename, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    main_tag = soup.find('main')
    body_tag = soup.find('body')

    if not main_tag or not body_tag:
        print(f"❌ <main> ou <body> manquant dans {filename}, ignoré.")
        continue

    if soup.find('div', id='footer-container'):
        print(f"✅ Footer déjà présent dans {filename}, ignoré.")
        continue

    # Créer le footer et l’ajouter après <main>
    footer = soup.new_tag('div', id='footer-container')
    main_tag.insert_after(footer)

    # Sauvegarder le fichier sans .bak
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(str(soup))

    print(f"✅ Footer ajouté dans {filename}")

print("\n🎉 Terminé !")
