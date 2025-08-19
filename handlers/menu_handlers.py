from telegram import (
    Update, ReplyKeyboardMarkup, KeyboardButton, InputFile,
    InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
)
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters, CallbackQueryHandler
)
from utils.helpers import *
from handlers.cv_handlers import *
from handlers.models_handlers import *
from bank_text import *
from Config import *



# ============================
# 🌐 Commande /start et Menu Principal
# ============================
import random

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_name = update.effective_user.full_name

    # 🎭 Messages d’accueil fun pour toi
    test_messages = [
        "🎯 Mr, les propulseurs sont prêts... Jarvis est en ligne.",
        "🛠️ Chargement de l’armure Mark 85... prêt pour un test ?",
        "⚡ Activation du mode WakandaTech... Shuri est dans la place 😏",
        "🚀 Démarrage du CV-bot, Mr Stark. Tous les systèmes sont opérationnels.",
        "🎬 On y va Boss ! Et n'oublie pas : *I am Iron Bot*."
    ]

    # 📡 Messages d’alerte fun pour un nouvel utilisateur
    alert_messages = [
        f"🚨 Boss, on a un intrus... euh, un nouvel utilisateur : **{user_name}** (ID: {user_id}).",
        f"📡 Nouveau signal détecté : {user_name} vient d’entrer dans le Wakanda numérique.",
        f"⚡ {user_name} s’est connecté... je prépare un CV plus stylé que la tenue de Black Panther.",
        f"🕶️ {user_name} vient de pousser la porte... je sors l’armure ?",
        f"🛰️ Transmission reçue... {user_name} est maintenant dans la base de données."
    ]

    # Si ce n’est pas toi → on prévient l’admin
    if user_id != YOUR_USER_ID:
        text = get_users_list_text()
        await context.bot.send_message(chat_id=YOUR_USER_ID, text=random.choice(alert_messages), parse_mode="Markdown")
        await context.bot.send_message(chat_id=CHANNEL_ID, text=text)
        #await update.message.reply_text(f"Sessions : {str(sessions)} et user_id : {str(user_id)}")

    # Si c’est toi → message de test aléatoire
    else:
        await update.message.reply_text(random.choice(test_messages), parse_mode="Markdown")

    # Menu principal
    keyboard = [
        [KeyboardButton("📝 Créer un CV"), KeyboardButton("📄 Voir un exemple")],
        [KeyboardButton("⚙️ Aide")],
        [KeyboardButton("🧽 Clean")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    # Image + présentation
    with open('Assets/CV_bot.jpeg', 'rb') as photo:
        await update.message.reply_photo(
            photo=photo,
            caption=f"👋 Bienvenue **{user_name}**, je suis CV-bot, ton assistant personnel. "
                    f"On va rendre ton CV plus classe qu'une armure StarkTech. 😎",
            parse_mode="Markdown"
        )

    await update.message.reply_text("Alors, par quoi on commence ?", reply_markup=reply_markup)

# ====================
# 📊 Gestion des messages
# ====================
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.message.from_user.id
    session = get_session(user_id)

    if text == "📝 Créer un CV":
        session.step = 0
        await update.message.reply_text("Super ! Commençons la création du CV.")
        await event_CVbuilding_text(update, context)
        #await handle_message(update, context)

    elif text in ["🧾 Simple (ATS)", "🎯 Moderne", "🎨 Créatif"]:
        keyboard = [[KeyboardButton("🔙 Go back")]]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text("📂 Tu peux revenir au menu de départ si tu veux !!!", reply_markup=reply_markup)
        #await   #await see_modele(Update, context)
        await event_CVbuilding(update, context)
        

    elif text == "🔙 Go back":
        keyboard = [
            [KeyboardButton("📝 Créer un CV"), KeyboardButton("📄 Voir un exemple")],
            [KeyboardButton("⚙️ Aide")],
            [KeyboardButton("🧽 Clean")]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text("Vous êtes au menu départ ?", reply_markup=reply_markup)
        


    elif text == "⚙️ Aide":
        await update.message.reply_text(texte_aide, parse_mode="Markdown")
        await infos(update, context)

    elif text == "❌ Quitter":
        await update.message.reply_text("Merci et à bientôt !")

    elif text == "🧽 Clean":
        #await update.message.reply_text(f"Sessions : {str(sessions)} et user_id : {str(user_id)}")
        if user_id in sessions:
            del sessions[user_id]
        await update.message.reply_text("Données utilisateur réinitialisées.", reply_markup=ReplyKeyboardMarkup([
            [KeyboardButton("📝 Créer un CV"), KeyboardButton("📄 Voir un exemple")],
            [KeyboardButton("⚙️ Aide")],
            [KeyboardButton("🧽 Clean")]
        ], resize_keyboard=True))

    else:
        if session.step >= 1:
            await event_CVbuilding(update, context)
        else:
            await update.message.reply_text("Commande non reconnue. Choisis un bouton dans le menu.")



def setup_menu_handlers(app):
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
