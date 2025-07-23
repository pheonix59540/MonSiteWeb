from PIL import Image
import os

# Extensions d'images à prendre en charge
valid_extensions = ['.png', '.bmp', '.jpeg', '.jpg', '.JPG']

# Liste tous les fichiers du dossier courant
for filename in os.listdir('.'):
    name, ext = os.path.splitext(filename)
    
    if ext.lower() in valid_extensions:
        try:
            # Ouvre l'image
            with Image.open(filename) as img:
                # Convertit en mode RGB si nécessaire (utile pour PNG avec transparence)
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Nouveau nom avec extension .jpg
                new_name = name + '.jpg'

                # Sauvegarde l'image convertie
                img.save(new_name, format='JPEG', quality=95)

                print(f"✅ {filename} → {new_name}")
        except Exception as e:
            print(f"❌ Erreur avec {filename} : {e}")
