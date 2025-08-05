
from PIL import Image
import os

import imgkit

def html_to_linkedin_image(html_path, output_folder="images", target_size=(627, 1200)):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Génère une image temporaire à partir du HTML
    image_path = os.path.join(output_folder, os.path.basename(html_path).replace(".html", "_linkedin.jpg"))
    
    options = {
        "format": "jpg",
        "crop-h": str(target_size[1]),
        "crop-w": str(target_size[0]),
        "quality": "95",
        "encoding": "UTF-8",
        "enable-local-file-access": "",  # nécessaire pour lire les fichiers CSS locaux
    }

    imgkit.from_file(html_path, image_path, options=options)
    return image_path


def resize_with_padding(image, target_size):
    target_width, target_height = target_size
    img_ratio = image.width / image.height
    target_ratio = target_width / target_height

    if img_ratio > target_ratio:
        # Image trop large → redimensionner largeur
        new_width = target_width
        new_height = int(target_width / img_ratio)
    else:
        # Image trop haute → redimensionner hauteur
        new_height = target_height
        new_width = int(target_height * img_ratio)

    resized = image.resize((new_width, new_height), Image.LANCZOS)

    # Créer un fond blanc à la bonne taille
    result = Image.new("RGB", target_size, (255, 255, 255))
    pos_x = (target_width - new_width) // 2
    pos_y = (target_height - new_height) // 2
    result.paste(resized, (pos_x, pos_y))
    return result
