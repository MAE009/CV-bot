import random

MESSAGES = [
    "📌 CV Builder est toujours en ligne !",
    "🛠️ Le générateur de CV fonctionne, testez-le dès maintenant.",
    "📄 Besoin d’un CV ? Envoyez /start au bot !",
    "⏳ Ping automatique pour garder CV Builder actif.",
]

def keep_alive(token, channel_id):
    from telegram import Bot
    import threading

    bot = Bot(token)
    message = random.choice(MESSAGES)
    bot.send_message(chat_id=channel_id, text=message)

    # Relancer après 10 minutes
    threading.Timer(600, keep_alive, args=(token, channel_id)).start()


"""
import threading
from telegram import Bot

def keep_alive(bot_token, channel_id):
    bot = Bot(token=bot_token)
    bot.send_message(chat_id=channel_id, text="✅ Bot actif : ping toutes les 28 min.")
    # Relancer la fonction dans 1680 secondes (28 min)
    threading.Timer(1680, keep_alive, args=[bot_token, channel_id]).start()
"""
