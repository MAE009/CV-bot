import os
import asyncio
import nest_asyncio
from flask import Flask
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

nest_asyncio.apply()

flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "✅ Bot Telegram CV en ligne !"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [KeyboardButton("📝 Créer un CV"), KeyboardButton("📄 Voir un exemple")],
        [KeyboardButton("⚙️ Aide"), KeyboardButton("❌ Quitter")],
        [KeyboardButton("🧽 Clean")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    # 1. Envoie du message de bienvenue
    #await update.message.reply_text("👋 Bienvenue, je suis CV-bot ! Que veux-tu faire ?", reply_markup=reply_markup)

    # 2. Envoi de l'image juste après le message
    with open('CV_bot.jpeg', 'rb') as photo:
        await update.message.reply_photo(photo=photo, caption="👋 Bienvenue, je suis CV-bot ! Que veux-tu faire ?")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "📝 Créer un CV":
        await update.message.reply_text("Super ! Commençons. Quel est ton prénom ?")
    elif text == "📄 Voir un exemple":
        await update.message.reply_text("Voici un exemple de CV fictif : Jean Dupont, développeur Python...")
    elif text == "⚙️ Aide":
        await update.message.reply_text("Je suis là pour t’aider à créer un CV étape par étape.")
    elif text == "❌ Quitter":
        await update.message.reply_text("Merci et à bientôt !")
    else:
        await update.message.reply_text("Commande non reconnue. Choisis un bouton dans le menu.")

async def run():
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Lancer le bot Telegram
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    
    # Lancer Flask (dans une boucle parallèle)
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, lambda: flask_app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000))))

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(run())
