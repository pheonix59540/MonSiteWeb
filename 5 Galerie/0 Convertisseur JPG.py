from PIL import Image
import os

# Parcours de tous les fichiers dans le dossier courant
for filename in os.listdir('.'):
    if filename.lower().endswith(('.jpg', '.jpeg', '.JPG', '.JPEG')):
        base_name, ext = os.path.splitext(filename)
        new_filename = base_name + '.jpg'

        try:
            # Ouvre l'image avec Pillow
            with Image.open(filename) as img:
                # Convertit en mode RGB pour compatibilité JPG
                rgb_image = img.convert('RGB')
                # Sauvegarde sous nouveau fichier .jpg
                rgb_image.save(new_filename, format='JPEG')
            # Supprime l'ancien fichier
            if filename != new_filename:
                os.remove(filename)
            print(f"✔️ Converti et corrigé : {filename} → {new_filename}")
        except Exception as e:
            print(f"⚠️ Erreur avec {filename} : {e}")
