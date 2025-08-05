
from PIL import Image
import os

import imgkit

def html_to_linkedin_image_1(html_path, output_folder="images", target_size=(627, 1200)):
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
import os
import imgkit

def html_to_linkedin_image(html_path, output_folder="images", target_size=(1200, 627)):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 🔄 Injecter automatiquement le CSS depuis le même répertoire
    injected_html = inject_css_from_same_path(html_path)

    image_path = os.path.join(
        output_folder,
        os.path.basename(html_path).replace(".html", "_linkedin.jpg")
    )

    options = {
        "format": "jpg",
        "crop-h": str(target_size[1]),
        "crop-w": str(target_size[0]),
        "quality": "95",
        "encoding": "UTF-8",
        "enable-local-file-access": "",  # important
    }

    imgkit.from_file(injected_html, image_path, options=options)
    return image_path

def inject_css_from_same_path(html_path):
    css_path = html_path.replace(".html", ".css")

    # Lire le HTML
    with open(html_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    # Lire le CSS (si existe)
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            css_content = f.read()
        
        # Injecter dans <head>
        if "<head>" in html_content:
            html_content = html_content.replace(
                "<head>", f"<head>\n<style>\n{css_content}\n</style>\n"
            )
        else:
            html_content = f"<style>\n{css_content}\n</style>\n" + html_content
    else:
        print(f"⚠️ CSS non trouvé pour {html_path}")

    # Sauvegarder un nouveau fichier temporaire avec CSS intégré
    injected_path = html_path.replace(".html", "_injected.html")
    with open(injected_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    return injected_path

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
