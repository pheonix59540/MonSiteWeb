from PIL import Image
import os

# Récupérer tous les fichiers à la racine
for filename in os.listdir('.'):
    # Identifier les fichiers .JPG ou .JPEG
    if filename.lower().endswith('.jpg') or filename.lower().endswith('.jpeg'):
        with Image.open(filename) as img:
            # Créer un nouveau nom de fichier en .jpg en minuscules
            new_filename = os.path.splitext(filename)[0] + '.jpg'

            # Sauvegarder l'image au bon format (JPEG)
            img.convert('RGB').save(new_filename, 'JPEG')

        # Si le nom original est différent du nouveau (ex: .JPG → .jpg), supprimer l'ancien
        if filename != new_filename:
            os.remove(filename)
            print(f'Converti et remplacé : {filename} → {new_filename}')
        else:
            print(f'Pas besoin de renommer : {filename}')
