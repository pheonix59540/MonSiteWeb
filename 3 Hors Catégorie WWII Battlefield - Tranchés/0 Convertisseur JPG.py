from PIL import Image
import os

# Dossier à traiter (ici : la racine du script)
folder = "."

# Extensions d'images à convertir
extensions = (
    ".png",
    ".avif",
    ".webp",
    ".bmp",
    ".tif",
    ".tiff",
    ".gif",
    ".jpeg",
    ".jpg",
)

# Parcours tous les fichiers du dossier
for filename in os.listdir(folder):

    # Ignore les fichiers qui ne sont pas des images
    if not filename.lower().endswith(extensions):
        continue

    # Ignore les JPG déjà existants
    if filename.lower().endswith(".jpg") or filename.lower().endswith(".jpeg"):
        continue

    image_path = os.path.join(folder, filename)
    jpg_path = os.path.join(
        folder,
        os.path.splitext(filename)[0] + ".jpg"
    )

    try:
        # Ouverture de l'image
        with Image.open(image_path) as img:

            # Gestion des images avec transparence
            if img.mode in ("RGBA", "LA", "P"):
                background = Image.new("RGB", img.size, "white")

                if img.mode == "P":
                    img = img.convert("RGBA")

                background.paste(img, mask=img.getchannel("A"))
                img = background

            else:
                img = img.convert("RGB")

            # Sauvegarde en JPG
            img.save(
                jpg_path,
                "JPEG",
                quality=95,
                optimize=True
            )

        print(f"Converti : {filename} → {os.path.basename(jpg_path)}")

    except Exception as e:
        print(f"ERREUR : {filename} → {e}")

print("Conversion terminée.")