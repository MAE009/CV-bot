from flask import Flask
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import threading
import os

# Flask app (nécessaire pour Render)
flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "✅ Le bot est en ligne !"

# --- Bot Telegram ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [KeyboardButton("📝 Créer un CV"), KeyboardButton("📄 Voir un exemple")],
        [KeyboardButton("⚙️ Aide"), KeyboardButton("❌ Quitter")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("👋 Bienvenue ! Que veux-tu faire ?", reply_markup=reply_markup)

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

def run_bot():
    TELEGRAM_BOT_TOKEN=7652152321:AAGnR9dzEbyd8mUfeeQR-ZMrEacoR28R_eU
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

# --- Lancement parallèle du bot + serveur Flask ---
if __name__ == '__main__':
    threading.Thread(target=run_bot).start()
    flask_app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
