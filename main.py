# 📦 Imports
import os
import asyncio
import nest_asyncio
from flask import Flask
from telegram import (
    Update, ReplyKeyboardMarkup, KeyboardButton, InputFile,
    InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
)
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
)

from cvbuilder import CVBuilder  # Générateur de CV
from user import *  # Fonctions utilisateur
from bank_text import *  # Textes prédéfinis (conseils, résumés...)

# ====================
# 🌐 Variables Globales
# ====================
sessions = {}  # Stocke les sessions utilisateur
YOUR_USER_ID = 5227032520  # Votre ID
CHANNEL_ID = "@Temoignage_Service_M_A_E005"  # Canal Telegram

# ====================
# ✨ Fonctions Utilitaires
# ====================
def get_session(user_id):
    if user_id not in sessions:
        sessions[user_id] = CVBuilder()
    return sessions[user_id]

# ====================
# 🔧 Handlers Principaux
# ====================
async def infos(update, context):
    web_app_url = "https://cv-bot-infos.onrender.com"
    keyboard = [[InlineKeyboardButton("🌐 Ouvrir la Web App", web_app=WebAppInfo(url=web_app_url))]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "🛠️ Clique sur le bouton ci-dessous pour ouvrir l’aide dans la Web App :",
        reply_markup=reply_markup
    )

async def get_id_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat
    await update.message.reply_text(
        f"🧑‍💻 Ton ID utilisateur : `{user.id}`\n"
        f"💬 Type de chat : `{chat.type}`\n"
        f"🔚 Chat ID (si tu envoies cette commande depuis un canal ou groupe) : `{chat.id}`",
        parse_mode="Markdown"
    )

async def send_users_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id == YOUR_USER_ID:
        text = get_users_list_text()
        await context.bot.send_message(chat_id=CHANNEL_ID, text=text)
        await update.message.reply_text("✅ Liste envoyée au canal !")
    else:
        await update.message.reply_text("🚫 Accès refusé.")

# =========================
# 📁 Flask pour Webhook Info
# =========================
nest_asyncio.apply()
flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "✅ Bot Telegram CV en ligne !"

# ============================
# 🌐 Commande /start et Menu Principal
# ============================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [KeyboardButton("📝 Créer un CV"), KeyboardButton("📄 Voir un exemple")],
        [KeyboardButton("⚙️ Aide"), KeyboardButton("❌ Quitter")],
        [KeyboardButton("🧽 Clean")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    with open('Assets/CV_bot.jpeg', 'rb') as photo:
        await update.message.reply_photo(photo=photo, caption="👋 Bienvenue, je suis CV-bot !")
        await update.message.reply_text("Que veux-tu faire 😄?", reply_markup=reply_markup)

# ====================
# 🚧 Générateur de CV (PDF)
# ====================
async def generator(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await update.message.reply_text("🛠️ Génération de ton CV en cours... ⏳")
        file_path = session.simple_cv()
        with open(file_path, "rb") as file:
            await update.message.reply_document(
                document=InputFile(file),
                filename=os.path.basename(file_path),
                caption="✅ Voici ton CV tout beau, tout propre ! 💼\nTu peux le télécharger et l’utiliser directement."
            )
    except Exception as e:
        await update.message.reply_text(f"❌ Une erreur est survenue : {e}")
        print("Erreur :", e)

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
        await event_CVbuilding(update, context)

    elif text == "📄 Voir un exemple":
        await update.message.reply_text("Voici un exemple de CV fictif : Jean Dupont, développeur Python...")

    elif text == "⚙️ Aide":
        await update.message.reply_text(texte_aide, parse_mode="Markdown")
        await infos(update, context)

    elif text == "❌ Quitter":
        await update.message.reply_text("Merci et à bientôt !")

    elif text == "🧽 Clean":
        if user_id in sessions:
            del sessions[user_id]
        await update.message.reply_text("Données utilisateur réinitialisées.", reply_markup=ReplyKeyboardMarkup([
            [KeyboardButton("📝 Créer un CV"), KeyboardButton("📄 Voir un exemple")],
            [KeyboardButton("⚙️ Aide"), KeyboardButton("❌ Quitter")],
            [KeyboardButton("🧽 Clean")]
        ], resize_keyboard=True))

    else:
        if session.step >= 1:
            await event_CVbuilding(update, context)
        else:
            await update.message.reply_text("Commande non reconnue. Choisis un bouton dans le menu.")

# ======================
# 🎓 Lancement du bot + Webhook
# ======================
async def run():
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("sendusers", send_users_command))
    app.add_handler(CommandHandler("id", get_id_command))
    app.add_handler(CommandHandler("gr", generator))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    await app.initialize()
    await app.start()
    await app.updater.start_polling()

    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, lambda: flask_app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000))))

# ======================
# ⭐ Point d'entrée du script
# ======================
if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(run())
