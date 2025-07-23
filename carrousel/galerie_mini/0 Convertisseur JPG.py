from PIL import Image
import os

# Extensions reconnues comme images
valid_extensions = ['.png', '.bmp', '.jpeg', '.jpg', '.JPG']

# Parcours du dossier courant
for filename in os.listdir('.'):
    name, ext = os.path.splitext(filename)
    ext = ext.lower()

    if ext in valid_extensions:
        try:
            # Ouvrir l'image
            with Image.open(filename) as img:
                # Vérifie et convertit le mode (ex: PNG avec transparence)
                if img.mode != 'RGB':
                    img = img.convert('RGB')

                # Nouveau nom avec extension .jpg (vraie conversion)
                new_name = name + '.jpg'

                # Sauvegarde en format JPEG
                img.save(new_name, format='JPEG', quality=95)

            # Supprime l'ancienne image si son nom diffère (évite d'effacer une vraie .jpg déjà convertie)
            if filename != new_name:
                os.remove(filename)
                print(f"✅ {filename} converti → {new_name} (et original supprimé)")
            else:
                print(f"✅ {filename} est déjà en .jpg, reconverti proprement")

        except Exception as e:
            print(f"❌ Erreur sur {filename} : {e}")
