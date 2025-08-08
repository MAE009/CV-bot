import asyncio
from telegram import (
    Update, ReplyKeyboardMarkup, KeyboardButton, InputFile,
    InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
)
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters, CallbackQueryHandler
)

from cvbuilder import CVBuilder  # Générateur de CV
from user import *  # Fonctions utilisateur
from Config import *



def get_session(user_id):
    if user_id not in sessions:
        sessions[user_id] = CVBuilder()
    return sessions[user_id]


async def infos(update, context):
    web_app_url = "https://cv-bot-infos.onrender.com"
    keyboard = [[InlineKeyboardButton("🌐 Ouvrir la Web App", web_app=WebAppInfo(url=web_app_url))]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "🛠️ Clique sur le bouton ci-dessous pour ouvrir l’aide dans la Web App :",
        reply_markup=reply_markup
    )


async def get_id_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat
    await update.message.reply_text(
        f"🧑‍💻 Ton ID utilisateur : `{user.id}`\n"
        f"💬 Type de chat : `{chat.type}`\n"
        f"🔚 Chat ID (si tu envoies cette commande depuis un canal ou groupe) : `{chat.id}`",
        parse_mode="Markdown"
    )


async def send_users_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id == YOUR_USER_ID:
        text = get_users_list_text()
        await context.bot.send_message(chat_id=CHANNEL_ID, text=text)
        await update.message.reply_text("✅ Liste envoyée au canal !")
    else:
        await update.message.reply_text("🚫 Accès refusé.")


async def setup_helpers(app):
    app.add_handler(CommandHandler("sendusers", send_users_command))
    app.add_handler(CommandHandler("id", get_id_command))
    
