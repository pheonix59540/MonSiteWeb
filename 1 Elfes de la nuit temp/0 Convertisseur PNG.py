from PIL import Image
import os

# Dossier à traiter (ici : la racine du script)
folder = "."

# Parcours tous les fichiers du dossier
for filename in os.listdir(folder):
    if filename.lower().endswith(".png"):
        png_path = os.path.join(folder, filename)
        jpg_path = os.path.join(folder, os.path.splitext(filename)[0] + ".jpg")

        # Ouverture et conversion
        with Image.open(png_path) as img:
            # Conversion en mode RGB si nécessaire
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            img.save(jpg_path, "JPEG", quality=95)

        print(f"Converti : {filename} → {os.path.basename(jpg_path)}")

print("Conversion terminée.")
