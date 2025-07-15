import os  
import asyncio  
import nest_asyncio  
from cvbuilder import CVBuilder
from user import*
from descript import*
from flask import Flask  
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton  
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters  
  
# Variables globales  
begin_cv = False  
sessions = {}  
  
# Gestion des sessions utilisateur  
def get_session(user_id):  
    if user_id not in sessions:  
        sessions[user_id] = CVBuilder()  
    return sessions[user_id]  
  
nest_asyncio.apply()  
flask_app = Flask(__name__)


YOUR_USER_ID = 5227032520  # mon ID
CHANNEL_ID = "@Temoignage_Service_M_A_E005"  # mon canal

async def send_users_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id == YOUR_USER_ID:  # sécurité
        text = get_users_list_text()
        await context.bot.send_message(chat_id=CHANNEL_ID, text=text)
        await update.message.reply_text("✅ Liste envoyée au canal !")
    else:
        await update.message.reply_text("🚫 Accès refusé.")
  


@flask_app.route('/')  
def home():  
    return "✅ Bot Telegram CV en ligne !"  
  
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):  
    keyboard = [  
        [KeyboardButton("📝 Créer un CV"), KeyboardButton("📄 Voir un exemple")],  
        [KeyboardButton("⚙️ Aide"), KeyboardButton("❌ Quitter")],  
        [KeyboardButton("🧽 Clean")]  
    ]  
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)  
  
    with open('CV_bot.jpeg', 'rb') as photo:  
        await update.message.reply_photo(photo=photo, caption="👋 Bienvenue, je suis CV-bot !")  
        await update.message.reply_text("Que veux-tu faire 😄?", reply_markup=reply_markup)  


  
async def event_CVbuilding(update: Update, context: ContextTypes.DEFAULT_TYPE):  
    
    global session 
      
    
    user = update.message.from_user
    user_id = user.id
    session = get_session(user_id)
    save_user(user)
  
    await update.message.reply_text(session.step)
    if session.step <= 5 :
        #await update.message.reply_text(session)
        
        if session.step == 0:
            #session.update_info("nom", update.message.text)
            await update.message.reply_text("Partie N° 1 : l'entête 🪧")
            await update.message.reply_text("Quel est ton nom de famille ?")
            
            session.next_step()

        elif session.step == 1:
            session.update_info("nom", update.message.text)
            await update.message.reply_text("Quel est ton prénom ?")
            session.next_step()

        elif session.step == 2:
            session.update_info("prenom", update.message.text)
            await update.message.reply_text("Quel est le nom de ta ville ?")
            session.next_step()

        elif session.step == 3:
            session.update_info("ville", update.message.text)
            await update.message.reply_text("Quel est ton numéro de téléphone 📲 ?")
            session.next_step()

        elif session.step == 4:
            session.update_info("tel", update.message.text)
            await update.message.reply_text("Quel est ton adresse email 📧 ?")
            session.next_step()

        elif session.step == 5:
            session.update_info("email", update.message.text)
           # session.update_info("autre", update.message.text)
            keyboard = [[KeyboardButton("Non fourni")]]
            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            await update.message.reply_text("Quel est le lien ton compte LinkedIn ou ton site web ?", reply_markup=reply_markup)
            session.next_step()

    

    elif session.step == 6:
        text = update.message.text
        keyboard = [[KeyboardButton("🧽 Clean")]]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

        if text == "Non fourni" or text == "Je n'en ai pas !!!":
            autre = "❌ Non fourni"
            session.update_info("autre", autre)
        else:
            session.update_info("autre", text)
            autre = session.data["autre"]

        await update.message.reply_text(
        f"🧾 En-tête :\n"
        f"👤 {session.data['nom']} {session.data['prenom']}\n"
        f"📍 {session.data['ville']} || "
        f"📞 {session.data['tel']} || 📧 {session.data['email']}\n"
        f"🔗 {autre}",
        reply_markup=reply_markup
    )

        #session.next_step()
        #await update.message.reply_text("👉 On passe maintenant à la partie 2 : Objectif professionnel.")

        await update.message.reply_text("Partie N° 2 : le résumé 📜")

        await update.message.reply_text("""🎯 Petit conseil pour booster ton CV !

Tu n’as pas encore ajouté de résumé professionnel ? C’est dommage, car c’est souvent la première chose que les recruteurs lisent 👀.

💡 En 2-3 phrases (environ 50 à 100 mots), tu peux :
✅ Mettre en avant tes compétences clés
✅ Résumer ton expérience
✅ Montrer tes objectifs ou ambitions pro

Pense à cette section comme une pub express de toi-même 📣 — elle peut vraiment te faire sortir du lot ✨. Alors n’hésite pas à la rédiger pour capter l’attention en quelques secondes !
""")

        await update.message.reply_text("Vas-y, écris ✍️")
        session.next_step()

  
    elif session.step == 7:
        session.update_info("resume", update.message.text)
        await update.message.reply_text(
    "🎯 Résumé Professionnel\n{}\n{}\n{}".format(
        "="*30,
        session.data["resume"],
        "="*30
    )
)
        session.next_step()
     

  
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.message.from_user.id
    session = get_session(user_id)

    if text == "📝 Créer un CV":
        session.step = 0  # On recommence à zéro
        await update.message.reply_text("Super ! Commençons la création du CV.")
        await event_CVbuilding(update, context)

    elif text == "📄 Voir un exemple":
        await update.message.reply_text("Voici un exemple de CV fictif : Jean Dupont, développeur Python...")

    elif text == "⚙️ Aide":
        await update.message.reply_text(texte_aide, parse_mode="Markdown")

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
        # Si on est en pleine création de CV, continuer
        if session.step >= 1:
            await event_CVbuilding(update, context)
        else:
            await update.message.reply_text("Commande non reconnue. Choisis un bouton dans le menu.")




async def get_id_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat

    await update.message.reply_text(
        f"🧑‍💻 Ton ID utilisateur : `{user.id}`\n"
        f"💬 Type de chat : `{chat.type}`\n"
        f"🆔 Chat ID (si tu envoies cette commande depuis un canal ou groupe) : `{chat.id}`",
        parse_mode="Markdown"
    )






async def run():  
    token = os.getenv("TELEGRAM_BOT_TOKEN")  
    app = ApplicationBuilder().token(token).build()  
    app.add_handler(CommandHandler("start", start))  
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CommandHandler("sendusers", send_users_command))
    # Ajoute le handler :
    app.add_handler(CommandHandler("id", get_id_command))

  
    await app.initialize()  
    await app.start()  
    await app.updater.start_polling()  
  
    loop = asyncio.get_event_loop()  
    await loop.run_in_executor(None, lambda: flask_app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000))))  
  
if __name__ == '__main__':  
    asyncio.get_event_loop().run_until_complete(run())
