import os
import imgkit
from datetime import datetime

def html_to_linkedin_image(html_path, css_path=None, output_folder="linkedin_images", target_size=(1200, 627)):
    """Convertit un HTML en image optimisée pour LinkedIn"""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Préparer le chemin de sortie
    image_name = os.path.basename(html_path).replace(".html", "_linkedin.jpg")
    image_path = os.path.join(output_folder, image_name)

    # Options pour imgkit
    options = {
        "format": "jpg",
        "width": str(target_size[0]),
        "height": str(target_size[1]),
        "quality": "100",
        "enable-local-file-access": "",
        "encoding": "UTF-8",
    }

    # Si un CSS est spécifié, l'injecter
    if css_path and os.path.exists(css_path):
        options["user-style-sheet"] = css_path

    try:
        imgkit.from_file(html_path, image_path, options=options)
        print(f"🖼  Image LinkedIn générée: {image_path}")
        return image_path
    except Exception as e:
        print(f"❌ Erreur lors de la génération de l'image: {str(e)}")
        raise
