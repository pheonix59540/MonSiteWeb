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
        <h2>Donnez vie à vos colonies naines avec <strong>{titre}</strong> !</h2>
        <p>Plongez au cœur de l'artisanat et de la puissance naine avec <strong>{titre}</strong>, une pièce maîtresse de notre gamme <strong>Colonie Naine</strong>, conçue pour les passionnés de jeux fantastiques comme <strong>Warhammer Age of Sigmar, The Old World, 9th Age, Kings of War</strong>, et bien d'autres !</p>
        <p>Réalisée avec une qualité d'impression 3D exceptionnelle, ce décor détaillé, dessiné par <strong>Makers Anvil</strong>, ajoutera une dimension unique à vos champs de bataille. Que vous souhaitiez donner vie à une forteresse naine grouillante d'activité, créer un point stratégique pour vos armées ou simplement enrichir votre collection, <strong>{titre}</strong> est le complément idéal.</p>
        <p>Veuillez noter que le décor vous sera livré non assemblé et non peint, vous offrant la liberté de le personnaliser entièrement pour qu'il corresponde parfaitement à votre vision et à l'esthétique de vos armées !</p>
      </div>

      <div class="compatibilitySection">
        <h3>Et la taille dans tout ça ?</h3>
        <ul>
          <strong>{titre}</strong> n'est pas seulement une pièce maîtresse pour vos décors ; il est aussi pensé pour
          s'intégrer harmonieusement à vos jeux de figurines préférés. Avec des dimensions d'environ
          <strong>{dimension}</strong>, il offre un équilibre parfait entre encombrement sur la table et impact visuel.
        </ul>
      </div>

      <div class="contact-cta">
        <p>Envie de découvrir plus de créations issues de l'univers de <strong>Makers Anvil</strong>, ou d'autres décors fantastiques en plastique ?</p>
        <p>👉 <a href="../6 Contact.html">Contactez-nous directement</a> pour des demandes spécifiques ou des créations personnalisées !</p>
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
        <p><em>Photo non contractuelle. Décor à monter et à peindre.</em></p>
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
