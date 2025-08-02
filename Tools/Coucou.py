import random

PING_MESSAGES = [
    "🦾 Toujours vivant, pas encore remplacé par ChatGPT-5 !",
    "📄 J’attends vos CV comme un recruteur à la pause café.",
    "⏰ Je tourne en boucle, comme ton stagiaire préféré.",
    "🔧 Maintenance ? Nah, je suis parfait comme je suis.",
    "💾 Sauvegardé. Compressé. Toujours stylé.",
    "🧠 En pleine réflexion sur comment rendre ton CV 100x meilleur.",
    "👀 J’ai vu passer un /start. C’était un mirage ?",
    "📠 Ton générateur de CV préféré est sous caféine permanente.",
    "🤖 Je suis plus constant que ton Wi-Fi.",
    "🫠 Si je tombe, dis à Render que je l’aimais.",
    "📡 Ping-pong avec Render. Et je gagne !",
    "🎯 Objectif : un CV. Résultat : chef-d’œuvre !",
    "💬 Ce bot te parle toutes les X minutes juste pour ne pas mourir. C’est pas mignon ?",
    "🔥 Encore chaud bouillant pour générer du CV pro.",
    "🛸 Je suis un bot, pas un alien… quoique.",
    "🔋 Batterie à 100%. Motivation aussi.",
    "🎩 Ping magique envoyé. Je suis toujours là.",
    "🧙‍♂️ Sortilège de persistance activé : CV Builder ne meurt jamais.",
    "🧾 Tes CV me manquent. Reviens vite 😢",
    "🎭 Mon talent : générer des CV, pas faire des pauses."
]



import asyncio

def keep_alive(token, channel_id):
    async def send_ping():
        from telegram import Bot
        bot = Bot(token=token)

        while True:
            try:
                await bot.send_message(
                    chat_id=channel_id,
                    text=random.choice(PING_MESSAGES)
                )
            except Exception as e:
                print("Erreur keep_alive:", e)

            await asyncio.sleep(120)  # ⏱️ 2 minutes

    asyncio.ensure_future(send_ping())
