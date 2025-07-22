import os
from bs4 import BeautifulSoup

root_dir = '.'  # Répertoire racine
index_path = os.path.join(root_dir, 'index.html')

# 1. Lire index.html pour obtenir les pages listées dans <nav class="sidebar">
with open(index_path, 'r', encoding='utf-8') as f:
    index_html = f.read()

soup_index = BeautifulSoup(index_html, 'html.parser')
nav = soup_index.find('nav', class_='sidebar')
if not nav:
    print("❌ <nav class='sidebar'> non trouvé dans index.html")
    exit(1)

links = nav.find_all('a')
files_to_update = [link.get('href') for link in links if link.get('href')]

# 2. Parcourir chaque page listée dans la <nav>
for filename in files_to_update:
    file_path = os.path.join(root_dir, filename)
    if not os.path.isfile(file_path):
        print(f"⚠️ Fichier {filename} introuvable.")
        continue

    with open(file_path, 'r', encoding='utf-8') as f:
        file_html = f.read()

    soup = BeautifulSoup(file_html, 'html.parser')
    main_tag = soup.find('main')
    body_tag = soup.find('body')

    if not main_tag or not body_tag:
        print(f"⚠️
