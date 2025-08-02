import threading
from telegram import Bot

def keep_alive(bot_token, channel_id):
    bot = Bot(token=bot_token)
    bot.send_message(chat_id=channel_id, text="✅ Bot actif : ping toutes les 28 min.")
    # Relancer la fonction dans 1680 secondes (28 min)
    threading.Timer(1680, keep_alive, args=[bot_token, channel_id]).start()
