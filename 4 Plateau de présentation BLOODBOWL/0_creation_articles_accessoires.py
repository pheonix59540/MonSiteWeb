import os
import csv

def clean_filename(name):
    return name.replace(" ", " ").replace(",", ",").replace("'", "").replace("'", "").replace("é", "e").replace("à", "a")

def generate_html(data):
    if not data.get('titre'):  # ← minuscule
        return

    titre = data['titre'].strip()
    prix = data['prix'].strip().replace(' €', '€')
    dimension = data.get('dimension', '').strip()
    cheerleaders = data.get('cheerleaders', '').strip()
    big_guy = data.get('big_guy', '').strip()
    joueurs = data.get('joueurs', '').strip()
    option = data.get('Option', '').strip()  # ← 'Option' garde sa casse (majuscule dans le CSV)

    # Photos (jusqu'à 6 max)
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
  <h2>Optimisez vos matchs avec un plateau de présentation entièrement magnétique !</h2>

  <p>Découvrez <strong>{titre}</strong>, un plateau de jeu conçu pour offrir une organisation claire, fluide et immersive de vos équipes lors de vos parties de <strong>Blood Bowl</strong>.</p>

  <p>Entièrement pensé pour les coachs exigeants, ce plateau intègre un système <strong>full magnétique</strong> permettant de maintenir vos figurines en place tout au long du match. Fini les déplacements accidentels, les pertes de position ou les erreurs de comptage : chaque joueur trouve naturellement sa place sur le terrain.</p>

  <p>Chaque plateau est livré avec ses <strong>socles compatibles</strong> et propose une configuration adaptée à votre équipe avec un nombre défini de :</p>
  <ul>
    <li><strong>Joueurs</strong> : {joueurs}</li>
    <li><strong>Cheerleaders</strong> : {cheerleaders}</li>
    <li><strong>Big Guys</strong> : {big_guy}</li>
  </ul>

  <p>Vous pouvez également personnaliser votre expérience avec une option <strong>avec ou sans anneaux de compétence</strong>, idéals pour suivre facilement les capacités et états de vos joueurs en cours de match.</p>

  <p>Ce plateau est entièrement conçu pour s’adapter à vos besoins et rendre vos parties plus lisibles, rapides et immersives, que ce soit en compétition ou en jeu amical.</p>
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
with open("0_export_articles.csv", newline='', encoding='utf-8') as csvfile:  # ← underscore
    reader = csv.DictReader(csvfile, delimiter=';')
    for ligne in reader:
        generate_html(ligne)
