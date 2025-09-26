import os
import asyncio
from bank_text import *
from telegram import (
    Update, ReplyKeyboardMarkup, KeyboardButton, InputFile,
    InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
)
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters, CallbackQueryHandler
)
from cvbuilder import CVBuilder  # Générateur de CV
from Tools.Coucou import *
from Tools.capture_image import *
from utils.helpers import *




# Exemple de structure de templates
templates = {    
    "ATS": ["ats", "ats_classique", "ats_moderne", "ats_minimaliste"],    
    "Moderne": ["Mod1", "Mod2", "Mod3"],    
    "Créatif": ["Crea1", "Crea2", "Crea3"]    
}    

# Étape 1 - Voir les catégories
async def see_modele(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = []
    for category, template_list in templates.items():
        # Crée un bouton par template
        for template in template_list:
            button_text = f"{category} - {template}"
            callback_data = f"{category}|{template}"
            keyboard.append([InlineKeyboardButton(button_text, callback_data=callback_data)])

    reply_markup = InlineKeyboardMarkup(keyboard)      
    await update.message.reply_text(      
        "📌 Choisis un modèle de CV à générer :",      
        reply_markup=reply_markup      
    )

async def modele_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    try:
        print("DEBUG query.data =", query.data)  # 🔍 Debug

        parts = query.data.split("|")
        cv_type = parts[0]
        template_file = "|".join(parts[1:]) if len(parts) > 1 else None
        if not template_file:
            await query.edit_message_text("❌ Erreur: aucun template trouvé dans le callback_data")
            return

        session = get_session(query.from_user.id)

        await query.edit_message_text(f"⚙️ Génération du CV {cv_type}...")

        # Génération des fichiers
        pdf_path, image_path = session.test_modern_cv_generator(cv_type, template_file)

        # Envoi du PDF
        with open(pdf_path, "rb") as pdf_file:
            await context.bot.send_document(
                chat_id=query.message.chat.id,
                document=InputFile(pdf_file),
                caption="📄 Ton CV prêt à imprimer/envoyer"
            )

        # Envoi de l'image LinkedIn
        with open(image_path, "rb") as img_file:
            await context.bot.send_photo(
                chat_id=query.message.chat.id,
                photo=InputFile(img_file),
                caption="✨ Version optimisée pour LinkedIn"
            )

    except Exception as e:
        await context.bot.send_message(
            chat_id=query.message.chat.id,
            text=f"❌ Erreur: {str(e)}"
        )
        print(f"Erreur callback: {str(e)}")

def setup_models_handlers(app):
    app.add_handler(CommandHandler("voir_modeles", see_modele))
    app.add_handler(CallbackQueryHandler(modele_callback))
