import os
from PIL import Image, ExifTags

# Chemins
racine = os.getcwd()
source_folder = os.path.join(racine, "galerie")
output_folder = os.path.join(racine, "galerie_mini")
os.makedirs(output_folder, exist_ok=True)

# Extensions acceptées
extensions = ['.jpg', '.jpeg', '.png']

# Gestion de l'orientation EXIF
def correct_orientation(image):
    try:
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                break

        exif = image._getexif()
        if exif:
            orientation_value = exif.get(orientation, None)
            if orientation_value == 3:
                image = image.rotate(180, expand=True)
            elif orientation_value == 6:
                image = image.rotate(270, expand=True)
            elif orientation_value == 8:
                image = image.rotate(90, expand=True)
    except Exception:
        pass
    return image

# Génération HTML
html_output = ""

for filename in os.listdir(source_folder):
    name, ext = os.path.splitext(filename)
    if ext.lower() in extensions:
        try:
            image_path = os.path.join(source_folder, filename)
            img = Image.open(image_path)
            img = correct_orientation(img)

            # Réduction de la taille (optionnel : à adapter)
            img.thumbnail((1200, 1200))  # Limite max en px

            # Conversion et sauvegarde (JPEG léger par défaut)
            output_name = f"{name}.jpg"
            output_path = os.path.join(output_folder, output_name)
            img.save(output_path, format="JPEG", quality=70, optimize=True)

            # Ligne HTML correspondante
            html_output += f'<img src="carrousel/galerie_mini/{output_name}" alt="{name}" loading="lazy">\n'

        except Exception as e:
            print(f"Erreur avec {filename} : {e}")

# Écriture du fichier HTML
html_file_path = os.path.join(output_folder, "galerie.html")
with open(html_file_path, "w", encoding="utf-8") as f:
    f.write(html_output)

print("Conversion terminée. Fichier HTML généré dans 'galerie_mini'.")
