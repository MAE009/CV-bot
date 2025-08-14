# 📦 Imports
import os
import asyncio
import nest_asyncio
from flask import Flask
from telegram.ext import ApplicationBuilder
from handlers import setup_handlers
from Config import *
from utils.helpers import *
from Tools.Coucou import *



nest_asyncio.apply()
flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "✅ Bot Telegram CV en ligne !"
    

async def run():
    
    app = ApplicationBuilder().token(token).build()
    await setup_handlers(app)
    await setup_helpers(app)
    #await app.run_polling()
    await app.initialize()
    await app.start()
    await app.updater.start_polling()

    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, lambda: flask_app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000))))
  

if __name__ == '__main__':
    keep_alive(token, CHANNEL_ID)
    asyncio.get_event_loop().run_until_complete(run())
    
    
