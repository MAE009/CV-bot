from html2image import Html2Image
from PIL import Image
import os

def html_to_linkedin_image(html_path, output_folder="images", target_size=(1200, 627)):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    hti = Html2Image(output_path=output_folder)

    # Générer une image temporaire à partir du HTML
    tmp_name = "temp_preview.png"
    hti.screenshot(
        html_file=html_path,
        save_as=tmp_name,
        size=(target_size[0], target_size[1])  # base size
    )

    # Charger et redimensionner l'image finale
    temp_image_path = os.path.join(output_folder, tmp_name)
    image = Image.open(temp_image_path).convert("RGB")
    final_image = resize_with_padding(image, target_size)

    final_path = os.path.join(output_folder, "linkedin_preview.jpg")
    final_image.save(final_path, format="JPEG", quality=95)

    # Nettoyage du fichier temporaire
    os.remove(temp_image_path)

    return final_path


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
