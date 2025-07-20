import os
import asyncio
import nest_asyncio

from cvbuilder import CVBuilder
from user import *
from bank_text import *

from flask import Flask, request
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, InputFile, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters, ApplicationVariables globales

sessions = {}

#Gestion des sessions utilisateur

def get_session(user_id): if user_id not in sessions: sessions[user_id] = CVBuilder() return sessions[user_id]

nest_asyncio.apply() flask_app = Flask(name)

YOUR_USER_ID = 5227032520 CHANNEL_ID = "@Temoignage_Service_M_A_E005"

@flask_app.post("/webhook") def webhook() -> str: if flask_app.config.get("telegram_app"): telegram_app = flask_app.config["telegram_app"] else: return "App not configured", 500

update = Update.de_json(request.get_json(force=True), telegram_app.bot)
telegram_app.update_queue.put_nowait(update)
return "OK", 200

@flask_app.route('/') def home(): return "✅ Bot Telegram CV en ligne !"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE): keyboard = [ [KeyboardButton("📝 Créer un CV"), KeyboardButton("📄 Voir un exemple")], [KeyboardButton("⚙️ Aide"), KeyboardButton("❌ Quitter")], [KeyboardButton("🧽 Clean")] ] reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

with open('Assets/CV_bot.jpeg', 'rb') as photo:
    await update.message.reply_photo(photo=photo, caption="👋 Bienvenue, je suis CV-bot !")
    await update.message.reply_text("Que veux-tu faire 😄?", reply_markup=reply_markup)

async def infos(update, context): web_app_url = "https://cv-bot-infos.onrender.com" keyboard = [[ InlineKeyboardButton("🌐 Ouvrir la Web App", web_app=WebAppInfo(url=web_app_url)) ]] reply_markup = InlineKeyboardMarkup(keyboard)

await update.message.reply_text(
    "🛠️ Clique sur le bouton ci-dessous pour ouvrir l’aide dans la Web App :",
    reply_markup=reply_markup
)

async def get_id_command(update: Update, context: ContextTypes.DEFAULT_TYPE): user = update.effective_user chat = update.effective_chat

await update.message.reply_text(
    f"🧑‍💻 Ton ID utilisateur : `{user.id}`\n"
    f"💬 Type de chat : `{chat.type}`\n"
    f"🆔 Chat ID (si tu envoies cette commande depuis un canal ou groupe) : `{chat.id}`",
    parse_mode="Markdown"
)

async def send_users_command(update: Update, context: ContextTypes.DEFAULT_TYPE): user_id = update.effective_user.id if user_id == YOUR_USER_ID: text = get_users_list_text() await context.bot.send_message(chat_id=CHANNEL_ID, text=text) await update.message.reply_text("✅ Liste envoyée au canal !") else: await update.message.reply_text("🚫 Accès refusé.")

async def generator(update: Update, context: ContextTypes.DEFAULT_TYPE): try: await update.message.reply_text("🛠️ Génération de ton CV en cours... ⏳")

user_id = update.message.from_user.id
    session = get_session(user_id)
    file_path = session.simple_cv()

    with open(file_path, "rb") as file:
        await update.message.reply_document(
            document=InputFile(file),
            filename=os.path.basename(file_path),
            caption="✅ Voici ton CV tout beau, tout propre ! 💼\nTu peux le télécharger et l’utiliser directement."
        )

except Exception as e:
    await update.message.reply_text(f"❌ Une erreur est survenue lors de la création du CV 😞\nEssaye de recommencer ou contacte le support.\n{e}")
    print("Erreur :", e)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE): text = update.message.text user_id = update.message.from_user.id session = get_session(user_id)

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
    keyboard = [
        [KeyboardButton("📝 Créer un CV"), KeyboardButton("📄 Voir un exemple")],
        [KeyboardButton("⚙️ Aide"), KeyboardButton("❌ Quitter")],
        [KeyboardButton("🧽 Clean")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("Données utilisateur réinitialisées.", reply_markup=reply_markup)

else:
    if session.step >= 1:
        await event_CVbuilding(update, context)
    else:
        await update.message.reply_text("Commande non reconnue. Choisis un bouton dans le menu.")

async def run(): token = os.getenv("TELEGRAM_BOT_TOKEN") app = ApplicationBuilder().token(token).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.add_handler(CommandHandler("sendusers", send_users_command))
app.add_handler(CommandHandler("id", get_id_command))
app.add_handler(CommandHandler("gr", generator))
flask_app.config["telegram_app"] = app

await app.initialize()
await app.start()
await app.bot.set_webhook("https://cv-bot-46h5.onrender.com/webhook")

loop = asyncio.get_event_loop()
await loop.run_in_executor(None, lambda: flask_app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000))))

if name == 'main': asyncio.get_event_loop().run_until_complete(run())

