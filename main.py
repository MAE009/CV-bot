import os
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, InputFile, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from cvbuilder import CVBuilder
from user import *
from bank_text import *

# Sessions utilisateur
sessions = {}

def get_session(user_id):
    if user_id not in sessions:
        sessions[user_id] = CVBuilder()
    return sessions[user_id]

# Variables globales
YOUR_USER_ID = 5227032520
CHANNEL_ID = "@Temoignage_Service_M_A_E005"

# Commande /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [KeyboardButton("📝 Créer un CV"), KeyboardButton("📄 Voir un exemple")],
        [KeyboardButton("⚙️ Aide"), KeyboardButton("❌ Quitter")],
        [KeyboardButton("🧽 Clean")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    with open("Assets/CV_bot.jpeg", "rb") as photo:
        await update.message.reply_photo(photo=photo, caption="👋 Bienvenue, je suis CV-bot !")
        await update.message.reply_text("Que veux-tu faire 😄?", reply_markup=reply_markup)

# Commande /id
async def get_id_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat

    await update.message.reply_text(
        f"🧑‍💻 Ton ID utilisateur : `{user.id}`\n"
        f"💬 Type de chat : `{chat.type}`\n"
        f"🆔 Chat ID : `{chat.id}`",
        parse_mode="Markdown"
    )

# Commande /sendusers
async def send_users_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id == YOUR_USER_ID:
        text = get_users_list_text()
        await context.bot.send_message(chat_id=CHANNEL_ID, text=text)
        await update.message.reply_text("✅ Liste envoyée au canal !")
    else:
        await update.message.reply_text("🚫 Accès refusé.")

# Commande /gr
async def generator(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await update.message.reply_text("🛠️ Génération de ton CV en cours... ⏳")
        user_id = update.message.from_user.id
        session = get_session(user_id)
        file_path = session.simple_cv()

        with open(file_path, "rb") as file:
            await update.message.reply_document(
                document=InputFile(file),
                filename=os.path.basename(file_path),
                caption="✅ Voici ton CV tout beau, tout propre ! 💼"
            )
    except Exception as e:
        await update.message.reply_text(f"❌ Une erreur est survenue :\n{e}")
        print("Erreur :", e)

# Web App d’aide
async def infos(update, context):
    web_app_url = "https://cv-bot-infos.onrender.com"
    keyboard = [[InlineKeyboardButton("🌐 Ouvrir la Web App", web_app=WebAppInfo(url=web_app_url))]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "🛠️ Clique sur le bouton ci-dessous pour ouvrir l’aide dans la Web App :",
        reply_markup=reply_markup
    )

# Gestion des messages utilisateur
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
        await update.message.reply_text("✅ Données utilisateur réinitialisées.")

    else:
        if session.step >= 1:
            await event_CVbuilding(update, context)
        else:
            await update.message.reply_text("Commande non reconnue. Choisis un bouton dans le menu.")

# Lancement en mode polling
if __name__ == "__main__":
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise ValueError("❌ TELEGRAM_BOT_TOKEN n'est pas défini dans les variables d'environnement.")
    
    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("id", get_id_command))
    app.add_handler(CommandHandler("sendusers", send_users_command))
    app.add_handler(CommandHandler("gr", generator))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ Bot lancé en mode polling...")
    app.run_polling()
