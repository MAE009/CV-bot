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
# Exemple de structure de templates    
templates = {    
    "ATS": ["ats", "ats_classique", "ats_moderne", "ats_minimaliste"],    
    "Moderne": ["moderne1", "moderne2", "moderne3"],    
    "Créatif": ["creatif1", "creatif2", "creatif3"]    
}    

# Étape 1 - Voir les catégories
async def see_modele(update: Update, context: ContextTypes.DEFAULT_TYPE):    
    keyboard = [    
        [InlineKeyboardButton("📄 ATS", callback_data="category|ATS")],    
        [InlineKeyboardButton("🧩 Moderne", callback_data="category|Moderne")],    
        [InlineKeyboardButton("🎨 Créatif", callback_data="category|Créatif")]    
    ]    
    reply_markup = InlineKeyboardMarkup(keyboard)    
    
    await update.message.reply_text(    
        "📌 Choisis une catégorie de modèles :",    
        reply_markup=reply_markup    
    )    


# Étape 2 - Callback : si catégorie choisie, montrer les templates
async def modele_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    try:      
        parts = query.data.split("|")      
        action = parts[0]      

        if action == "category":      
            # category|ATS → 2 parties
            if len(parts) >= 2:
                category = parts[1]      
                keyboard = []      
                for template in templates[category]:      
                    button_text = template      
                    callback_data = f"template|{category}|{template}"      
                    keyboard.append([InlineKeyboardButton(button_text, callback_data=callback_data)])      

                reply_markup = InlineKeyboardMarkup(keyboard)      
                await query.edit_message_text(      
                    text=f"📂 Catégorie **{category}** : choisis un template",      
                    reply_markup=reply_markup,
                    parse_mode="Markdown"
                )
            else:
                await query.edit_message_text("❌ Format de callback invalide")

        elif action == "template":      
            # template|ATS|ats_classique → 3 parties
            if len(parts) >= 3:
                category = parts[1]      
                template_file = parts[2]      
                session = get_session(query.from_user.id)      

                await query.edit_message_text(f"⚙️ Génération du CV {category} ({template_file})...")      

                # Génération des fichiers      
                pdf_path, image_path = session.test_modern_cv_generator(category, template_file)      

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
            else:
                await query.edit_message_text("❌ Format de template invalide")

    except Exception as e:      
        await context.bot.send_message(      
            chat_id=query.message.chat.id,      
            text=f"❌ Erreur: {str(e)}"      
        )      
        print(f"Erreur callback: {str(e)}")
        

def setup_models_handlers(app):    
    app.add_handler(CommandHandler("voir_modeles", see_modele))    
    app.add_handler(CallbackQueryHandler(modele_callback))
