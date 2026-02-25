# 📦 Imports
import os
import asyncio
from flask import Flask
from telegram.ext import ApplicationBuilder
from handlers import setup_handlers
from Config import *
from utils.helpers import *
from Tools.Coucou import *

flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "✅ Bot Telegram CV en ligne !"

@flask_app.route('/health')
def health():
    return "OK", 200

async def run():
    """Fonction principale du bot"""
    app = ApplicationBuilder().token(token).build()
    await setup_handlers(app)
    await setup_helpers(app)
    
    # Démarrer le bot
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    
    # Démarrer Flask dans un thread séparé
    from threading import Thread
    def run_flask():
        flask_app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
    
    flask_thread = Thread(target=run_flask)
    flask_thread.start()
    
    # Garder le bot en vie
    while True:
        await asyncio.sleep(3600)  # 1 heure

if __name__ == '__main__':
    # Démarrer le keep_alive
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    # Lancer keep_alive en arrière-plan
    keep_alive(token, CHANNEL_ID)
    
    # Lancer le bot
    loop.run_until_complete(run())
