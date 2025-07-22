from flask import Flask, request
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackContext

flask_app = Flask(__name__)
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")  # Assure-toi que cette variable est définie dans Render

# Initialisation de l'application Telegram
application = ApplicationBuilder().token(TOKEN).build()

# Route pour le webhook
@flask_app.route('/webhook', methods=['POST'])
async def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    await application.process_update(update)
    return "OK", 200

# Route pour Uptime Robot (éviter la veille)
@flask_app.route('/health')
def health():
    return "OK", 200

# Commandes et handlers (ex: /start)
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Bot actif ✅")

application.add_handler(CommandHandler("start", start))

# Configuration du webhook au démarrage
async def set_webhook():
    WEBHOOK_URL = f"https://ton-bot.onrender.com/webhook"  # Remplace par ton URL Render
    await application.bot.set_webhook(WEBHOOK_URL)

if __name__ == '__main__':
    # Pour le développement local (polling)
    if os.getenv("ENV") == "dev":
        application.run_polling()
    else:
        # Pour Render (webhook)
        import asyncio
        loop = asyncio.get_event_loop()
        loop.run_until_complete(set_webhook())
        flask_app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
