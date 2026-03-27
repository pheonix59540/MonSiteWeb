import os
import csv

def clean_filename(name):
    return name.replace(" ", " ").replace(",", ",").replace("’", "").replace("'", "").replace("é", "e").replace("à", "a")

def generate_html(data):
    if not data.get('Titre'):  # Ignore les lignes vides
        return

    titre = data['Titre'].strip()
    prix = data['Prix'].strip().replace(' €', '€')
    dimension = data.get('Dimension', '').strip()

    # Photos (jusqu’à 6 max)
    photos = [data.get(f"Photo {i}", "").strip() for i in range(1, 7)]
    photos = [p for p in photos if p]

    # Nom du fichier
    nom_fichier = clean_filename(titre) + ".html"
    chemin = nom_fichier

    html =  f"""<!DOCTYPE html>
    <html lang="fr">
        <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{titre} - Décors</title>
        <link rel="stylesheet" href="../css/style.css">
        </head>
        <body>
            <header>
                </header>
        <main>
            <section class="gallery-article">
                <div class="product-header">
                    <h1>{titre}</h1>
                    <p class="price-article">{prix}</p>
                </div>

               <div class="descriptionSection">
        <h2>Optimisez Votre Expérience de Jeu avec <strong>{titre}</strong> !</h2>
        <p>Rangements astucieux, réglettes de mesure, organisateurs de dés, jetons et bien plus encore... chez <strong>Infinity3D</strong>, nous savons que le confort de jeu passe aussi par les petits détails. <strong>{titre}</strong> fait partie de notre gamme d'accessoires pratiques et esthétiques, conçus pour les passionnés de jeux de plateau, de wargames et de jeux de rôle.</p>
        <p>Imprimé avec soin et précision, <strong>{titre}</strong> allie fonctionnalité et style pour s'intégrer naturellement à votre table de jeu. Fini les dés qui roulent partout, les cartes mal rangées ou les jetons qui se perdent — chaque partie devient plus fluide et plus agréable !</p>
        <p>Cet accessoire vous sera livré prêt à l'emploi. Si vous souhaitez le personnaliser — peinture, patine, couleur spécifique — c'est tout à fait possible, laissez libre cours à votre créativité !</p>
      </div>

      <div class="compatibilitySection">
        <h3>Et la taille dans tout ça ?</h3>
        <ul>
          <strong>{titre}</strong> est conçu pour s'adapter facilement à votre espace de jeu. Avec des dimensions d'environ
          <strong>{dimension}</strong>, il trouve sa place aussi bien sur une grande table de wargame que sur un plateau de jeu de société plus compact.
          Pratique, discret et efficace !
        </ul>
      </div>

      <div class="contact-cta">
        <p>Vous avez un besoin spécifique ? Un accessoire sur mesure aux dimensions particulières, aux couleurs de votre armée ou adapté à un jeu précis ?</p>
        <p>👉 <a href="../6 Contact.html">Contactez-nous directement</a> pour des demandes personnalisées, on adore relever les défis !</p>
      </div>

      
"""

    if photos:
        html += '      <div class="gallery-details">\n'
        for photo in photos:
            nom_image = photo.strip()
            html += f'        <a href="LienPhoto/{nom_image}.html" target="_blank"><img src="{nom_image}.jpg" alt="{nom_image}"></a>\n'
        html += '      </div>\n'

    html += """    
        
        <div class="legal-notes">
        <p><em>Photo non contractuelle. Les couleurs peuvent varier selon les options choisies.</em></p>
        </div>
    
        </section>
        </main>
        </body>
        </html>
            """

    with open(chemin, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Fichier généré : {chemin}")

# Lecture du fichier CSV
with open("0 export_articles.csv", newline='', encoding='cp1252') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';')
    for ligne in reader:
        generate_html(ligne)
