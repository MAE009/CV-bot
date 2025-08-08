import os
import asyncio
from telegram.ext import ApplicationBuilder
from handlers import setup_handlers
from Config import *
from Tools.Coucou import *


async def main():
    
    app = ApplicationBuilder().token(token).build()
    await setup_handlers(app)
    #await app.run_polling()
    await app.initialize()
    await app.start()
    await app.updater.start_polling()

    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, lambda: flask_app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000))))
  

if __name__ == '__main__':
    
    keep_alive(token, CHANNEL_ID)
    asyncio.get_event_loop().run_until_complete(run())
    
    asyncio.run(main())
