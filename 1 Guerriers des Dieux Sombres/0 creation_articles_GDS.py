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
        <h2>Invoquez la puissance des Ténèbres : Les Guerriers des Dieux Sombres !</h2>
        <p>Plongez au cœur de l'indicible corruption et de la puissance brute avec cette figurine <strong>{titre}</strong>. Imprimées avec une fidélité inégalée en <strong>résine de haute qualité</strong>. Cettefigurine incarne la dévotion fanatique et la fureur déchaînée des forces du Chaos. Chaque pièce est un chef-d'œuvre de design, débordant de détails macabres, 
		de symboles hérétiques et de poses dynamiques qui capturent l'essence même de l'apocalypse.</p>
        <p>Issues de la vision audacieuse des sculpteurs <strong>de Lost Kingdom Miniatures</strong>, ces légions sont conçues pour apporter une présence intimidante 
		et une variété thématique sans précédent à vos collections et sur vos champs de bataille. 
		Qu'il s'agisse de démons hurlants, de fanatiques transfigurés ou de guerriers cuirassés, 
		chaque figurine est une ode à la gloire sombre de ses patrons divins.</p>
        <p>Cette figurine est livrée non-peinte et non-assemblée, vous offrant la liberté de les personnaliser <strong>et de les corrompre à votre guise, pour qu'elles s'intègrent parfaitement à vos armées .</strong></p>
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

      <a class="commande-cta" href="../6 Contact.html">
            <img class="commande-cta__icone" src="../images/enveloppe.svg" alt="" width="88" height="88">
            <span class="commande-cta__texte">
            <strong>Cet article vous plaît ?</strong>
            <span>Pour commander, écrivez-nous en précisant le nom de ou des articles et la quantité souhaitée.</span>
            </span>
            <span class="commande-cta__bouton">Nous contacter</span>
      </a>

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
