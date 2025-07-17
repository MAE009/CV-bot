import os  
import asyncio  
import nest_asyncio  
from cvbuilder import CVBuilder
from user import*
from bank_text import*
from flask import Flask  
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton  
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters  
  
# Variables globales
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

async def get_id_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat = update.effective_chat

    await update.message.reply_text(
        f"🧑‍💻 Ton ID utilisateur : `{user.id}`\n"
        f"💬 Type de chat : `{chat.type}`\n"
        f"🆔 Chat ID (si tu envoies cette commande depuis un canal ou groupe) : `{chat.id}`",
        parse_mode="Markdown"
    )


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
  
    with open('Assets/CV_bot.jpeg', 'rb') as photo:  
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

        await update.message.reply_text(header_summary(session.data, autre), reply_markup=reply_markup)

        #session.next_step()
        #await update.message.reply_text("👉 On passe maintenant à la partie 2 : Objectif professionnel.")

        await update.message.reply_text("Partie N° 2 : le résumé 📜")

        await update.message.reply_text(text_conseil_resume, parse_mode = "Markdown")

        await update.message.reply_text("Vas-y, écris ✍️")
        session.next_step()

  
    elif session.step == 7:
        session.update_info("resume", update.message.text)
        await update.message.reply_text(resume_summary(session.data), parse_mode="Markdown")
        await update.message.reply_text("Partie N° 3 : Expérience professionnelle 🧑‍💼")
        await update.message.reply_text(text_conseil_Exp, parse_mode="Markdown")
        await update.message.reply_text("Combien d'expériences veux-tu ajouter ? (Ex: 1, 2, 3...)")
        session.next_step()

    elif session.step == 8:
        try:
            session.nb_experiences = int(update.message.text)
            session.exp_index = 0
            session.current_exp = {}
            await update.message.reply_text(f"👉 Expérience {session.exp_index + 1} : Quel est l’intitulé du poste ?")
            session.step = 9
        except ValueError:
            await update.message.reply_text("❌ Entre un nombre valide (1, 2, 3...)")

    elif session.step == 9:
        session.current_exp["poste"] = update.message.text
        await update.message.reply_text("Quel est le nom de l’entreprise ?")
        session.step = 10

    elif session.step == 10:
        session.current_exp["entreprise"] = update.message.text
        await update.message.reply_text("Quelle est la période d’emploi ? (Ex: 2020 - 2023)")
        session.step = 11

    elif session.step == 11:
        session.current_exp["date"] = update.message.text
        await update.message.reply_text("Décris brièvement tes fonctions principales 📝")
        session.step = 12

    elif session.step == 12:
        session.current_exp["description"] = update.message.text
        await update.message.reply_text("Indique une ou deux réalisations clés 🎯")
        session.step = 13

    elif session.step == 13:
        session.current_exp["realisations"] = update.message.text
        session.experiences.append(session.current_exp.copy())  # Enregistrer l’expérience

        session.exp_index += 1
        if session.exp_index < session.nb_experiences:
            session.current_exp = {}
            await update.message.reply_text(f"👉 Expérience {session.exp_index + 1} : Quel est l’intitulé du poste ?")
            session.step = 9  # Recommencer à partir du titre du poste
        else:
            await update.message.reply_text("✅ Super, tu as terminé la section Expériences professionnelles !")
            session.next_step()  # maintenant step = 14
            await event_CVbuilding(update, context)
          
    elif session.step == 14:
        await update.message.reply_text(str(len(session.experiences)))
        await update.message.reply_text(experience_summary(session.experiences), parse_mode="Markdown")
        session.next_step()

  
    elif session.step == 15:
        await update.message.reply_text("Partie N° 4 : Formation 🎓")
        await update.message.reply_text(text_conseil_formation, parse_mode="Markdown")
        await update.message.reply_text("Combien de formations (diplômes ou certificats) veux-tu ajouter ? (ex : 2)")
        session.next_step()

    elif session.step == 16:
        try:
            session.nb_formations = int(update.message.text)
            session.format_index = 0
            session.current_format = {}
            await update.message.reply_text(f"👉 Formation {session.format_index + 1} : 1️⃣ Quel est l'intitulé du diplôme ou certificat ? (ex : BTS en Informatique)")
            session.step = 17
        except ValueError:
            await update.message.reply_text("❌ Entre un nombre valide (1, 2, 3...)")
          

    elif session.step == 17:
        session.current_format["diplôme"]=update.message.text
        await update.message.reply_text("2️⃣ Dans quel établissement l’as-tu obtenu ? (ex : Institut Technique de Pointe-Noire)")
        session.step = 18
      
    elif session.step == 18:
         session.current_format["établissement"]=update.message.text
         await update.message.reply_text("3️⃣ Quelle est l’année de début ? (ex : 2021)")
         session.step = 19
      
    elif session.step == 19:
        session.current_format["date_debut"]=update.message.text
        await update.message.reply_text("4️⃣ Et l’année de fin ? (ex : 2023)")
        session.step = 20
      
    elif session.step == 20:
        session.current_format["date_fin"]=update.message.text
        session.formations.append(session.current_format.copy())  # Enregistrer l’expérience

        session.format_index += 1
        if session.format_index < session.nb_formations:
            session.current_format = {}
            await update.message.reply_text(f"👉 Formation {session.format_index + 1} : 1️⃣ Quel est l'intitulé du diplôme ou certificat ? (ex : BTS en Informatique)")
            session.step = 17  # Recommencer à partir du titre du poste
        else:
            await update.message.reply_text("✅ Super, tu as terminé la section Formation !")
            session.next_step()  # maintenant step = 14
            await event_CVbuilding(update, context)
     
    
    elif session.step == 21:
        await update.message.reply_text(education_summary(session.formations), parse_mode="Markdown")




















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
