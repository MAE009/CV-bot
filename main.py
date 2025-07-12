import os  
import asyncio  
import nest_asyncio  
from cvbuilder import CVBuilder  
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
    global begin_cv  
    begin_cv = True  
    
    user_id = update.message.from_user.id  
    session = get_session(user_id)
  

    if session.step <= 5:
        

        if session.step == 0:
            session.update_info("nom", update.message.text)
            await update.message.reply_text("Partie N° 1 : l'entête 🪧")
            await update.message.reply_text("Quel est ton nom de famille ?")
            session.next_step()

        elif session.step == 1:
            session.update_info("prenom", update.message.text)
            await update.message.reply_text("Quel est ton prénom ?")
            session.next_step()

        elif session.step == 2:
            session.update_info("ville", update.message.text)
            await update.message.reply_text("Quel est le nom de ta ville ?")
            session.next_step()

        elif session.step == 3:
            session.update_info("tel", update.message.text)
            await update.message.reply_text("Quel est ton numéro de téléphone 📲 ?")
            session.next_step()

        elif session.step == 4:
            session.update_info("email", update.message.text)
            await update.message.reply_text("Quel est ton adresse email 📧 ?")
            session.next_step()

        elif session.step == 5:
            await update.message.reply_text("Quel est ton compte LinkedIn ou ton site web ?", reply_markup=reply_markup)
          
            session.update_info("autre", update.message.text)
            keyboard = [[KeyboardButton("Je n'en ai pas !!!")]]
            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            #await update.message.reply_text("Quel est ton compte LinkedIn ou ton site web ?", reply_markup=reply_markup)
          
            
            session.next_step()

    

    elif session.step == 6:
        keyboard = [[KeyboardButton("🧽 Clean")]]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        # Résumé de l’en-tête déjà rempli
        await update.message.reply_text(
            f"🧾 En-tête :\n"
            f"{session.data['nom']} {session.data['prenom']}\n"
            f"{session.data['ville']} || {session.data['tel']} || {session.data['email']} || {session.data.get('autre', 'N/A')}", reply_markup=reply_markup)


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
        # session.update_info("linkedin", update.message.text)  
        # await update.message.reply_text("Quel nombre d’années d’expérience as-tu ?")  
        # session.next_step()  


  
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):  
    text = update.message.text  
  
    if text == "📝 Créer un CV":  
        await update.message.reply_text("Super ! Commençons la création du CV.")  
        await event_CVbuilding(update, context)  
  
    elif text == "📄 Voir un exemple":  
        await update.message.reply_text("Voici un exemple de CV fictif : Jean Dupont, développeur Python...")  
  
    elif text == "⚙️ Aide":  
        await update.message.reply_text("Je suis là pour t’aider à créer un CV étape par étape.")  
  
    elif text == "❌ Quitter":  
        await update.message.reply_text("Merci et à bientôt !")  
  
    elif text == "🧽 Clean":  
        user_id = update.message.from_user.id  
        if user_id in sessions:  
            del sessions[user_id]
        keyboard = [  
        [KeyboardButton("📝 Créer un CV"), KeyboardButton("📄 Voir un exemple")],  
        [KeyboardButton("⚙️ Aide"), KeyboardButton("❌ Quitter")],  
        [KeyboardButton("🧽 Clean")]  
    ]  
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)  
  
        await update.message.reply_text("Données utilisateur réinitialisées.", reply_markup=reply_markup)  
  
    elif text == "Je n'en ai pas !!!":
        session.step += 1
        await update.message.reply_text("D'accord pas de problème")
      
    
    else:  
        # Continuer le processus CV si déjà commencé  
        user_id = update.message.from_user.id  
        session = get_session(user_id)  
        if begin_cv:  
            await event_CVbuilding(update, context)  
        else:  
            await update.message.reply_text("Commande non reconnue. Choisis un bouton dans le menu.")  
  
async def run():  
    token = os.getenv("TELEGRAM_BOT_TOKEN")  
    app = ApplicationBuilder().token(token).build()  
    app.add_handler(CommandHandler("start", start))  
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))  
  
    await app.initialize()  
    await app.start()  
    await app.updater.start_polling()  
  
    loop = asyncio.get_event_loop()  
    await loop.run_in_executor(None, lambda: flask_app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000))))  
  
if __name__ == '__main__':  
    asyncio.get_event_loop().run_until_complete(run())
