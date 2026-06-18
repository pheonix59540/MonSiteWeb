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
                <h2>Ne Perdez Plus le Fil de Vos Parties avec <strong>{titre}</strong> !</h2>
  <p>Stunned, Prone, Poisonné, Brûlé, Points de Vie... autant d'états et de statuts à suivre pendant vos parties qui peuvent vite devenir un casse-tête. Chez <strong>Infinity3D</strong>, nous avons conçu des marqueurs clairs, lisibles et esthétiques pour que vous ne perdiez plus jamais le fil de vos combats !</p>
  <p>Imprimé ou découpé au laser avec soin et précision, <strong>{titre}</strong> s'intègre naturellement à votre table de jeu. Fini les post-its qui s'envolent, les dés retournés en guise de compteurs ou les oublis en pleine mêlée — chaque marqueur est pensé pour être intuitif, durable et agréable à utiliser !</p>
  <p>Compatible avec de nombreux systèmes de jeu comme <strong>Blood Bowl, Warhammer Age of Sigmar, The Old World, 9th Age, Kings of War</strong> et bien d'autres. Ces marqueurs vous seront livrés prêts à l'emploi. Si vous souhaitez les personnaliser — peinture, couleur spécifique à votre armée — c'est tout à fait possible !</p>
</div>

<div class="compatibilitySection">
  <h3>Et la taille dans tout ça ?</h3>
  <ul>
    <strong>{titre}</strong> est conçu pour s'intégrer discrètement à côté de vos figurines sans encombrer votre table de jeu. Avec des dimensions d'environ
    <strong>{dimension}</strong>, il reste bien visible pendant la partie tout en prenant le minimum de place.
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
with open("0 export_articles.csv", newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';')
    for ligne in reader:
        generate_html(ligne)
