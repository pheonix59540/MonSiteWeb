import os
import csv

def clean_filename(name):
    return name.replace(" ", " ").replace(",", ",").replace("’", "").replace("'", "").replace("é", "e").replace("à", "a")

def generate_html(data):
    titre = data['Titre'].strip()
    prix = data['Prix'].strip().replace(' €', '€')
    socle_carre = data['Socle carré'].strip()
    socle_rond = data['Socle rond'].strip()

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
        <title>{titre} - Figurine</title>
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
        <h2>Une figurine imposante pour dominer le champ de bataille !</h2>
        <p>Découvrez <strong>{titre}</strong>, une superbe figurine imprimée en <strong>résine de haute qualité</strong>, conçue pour apporter toute la puissance et la brutalité des tribus ogres à vos armées fantastiques.</p>
        
        <p>Cette pièce est issue du travail remarquable des créateurs de <strong>The Lost Kingdom Miniatures</strong> et s'intègre parfaitement à l'univers féroce et nomade des <strong>Ogre Roroa Khans</strong>, où force, conquête et survie façonnent le destin des plus puissants guerriers.</p>
        
        <p>Cette figurine est livrée non-peinte et non-assemblée, prête à être personnalisée selon vos envies.</p>

      </div>

      <div class="compatibilitySection">
        <h3>Compatibilité des socles :</h3>
        <ul>
          <li><strong>Socle carré de {socle_carre if socle_carre else '—'}</strong> inclus. Idéal pour des jeux comme <strong>Warhammer Fantasy Battles</strong>, <strong>The Ninth Age (T9A)</strong>, <strong>Kings of War</strong>, ou tout autre jeu de figurines fantastique nécessitant des socles carrés !</li>
          <li>Besoin d'une option plus adaptée ? Disponible également en <strong>socle rond {socle_rond if socle_rond else '—'}</strong> Parfait pour s'adapter à d'autres formats de jeu ou pour des unités spécifiques.</li>
          **Nous pouvons également adapter le socle pour vos jeux avec socles ronds**, comme <strong>Age of Sigmar</strong>, <strong>Warhammer Underworlds</strong>, ou <strong>Malifaux</strong>. N'hésitez pas à nous contacter pour discuter des options !</li>
		  <li><strong> Attention, pour un même article,le prix peut varier s'il est proposé avec une scénique ou non.<strong>
        </ul>
      </div>

      <div class="contact-cta">
        <p>Envie de découvrir plus de créations issues de l'univers des Anciens Sauriens Remasterisés par The Lost Kingdom Miniatures, ou d'autres figurines fantastiques en résine ?</p>
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
        <p><em>Photo non contractuelle. Figurine à monter et sans socle autre que celui proposé.</em></p>
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
