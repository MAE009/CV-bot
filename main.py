# 📦 Imports
import os
import asyncio
import nest_asyncio
from flask import Flask
from telegram import (
    Update, ReplyKeyboardMarkup, KeyboardButton, InputFile,
    InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
)
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters, CallbackQueryHandler
)

from cvbuilder import CVBuilder  # Générateur de CV
from user import *  # Fonctions utilisateur
from bank_text import *  # Textes prédéfinis (conseils, résumés...)
from Tools.Coucou import *
from Tools.capture_image import *



# ====================
# 🌐 Variables Globales
# ====================
sessions = {}  # Stocke les sessions utilisateur
YOUR_USER_ID = 5227032520  # Votre ID
CHANNEL_ID = "@Temoignage_Service_M_A_E005"  # Canal Telegram

# ====================
# ✨ Fonctions Utilitaires
# ====================
def get_session(user_id):
    if user_id not in sessions:
        sessions[user_id] = CVBuilder()
    return sessions[user_id]

# ====================
# 🔧 Handlers Principaux
# ====================
# Debut New function

async def see_modele(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📄 Simple ATS", callback_data="ATS|ats")],
        [InlineKeyboardButton("🧩 Moderne", callback_data="Moderne|Mod")],
        [InlineKeyboardButton("🎨 Créatif", callback_data="Creative|Crea")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "📌 Choisis un modèle de CV à générer :",
        reply_markup=reply_markup
)

async def modele_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    try:
        cv_type, template_file = query.data.split("|")
        session = get_session(query.from_user.id)

        await query.edit_message_text(f"⚙️ Génération du CV {cv_type}...")

        # Génération des fichiers
        pdf_path, image_path = session.test_modern_cv_generator(cv_type, template_file)

        # Envoi du PDF
        with open(pdf_path, "rb") as pdf_file:
            await context.bot.send_document(
                chat_id=query.message.chat.id,
                document=InputFile(pdf_file),
                caption="📄 Ton CV prêt à imprimer/envoyer"
            )

        # Envoi de l'image LinkedIn
        with open(image_path, "rb") as img_file:
            await context.bot.send_photo(
                chat_id=query.message.chat.id,
                photo=InputFile(img_file),
                caption="✨ Version optimisée pour LinkedIn"
            )

    except Exception as e:
        await context.bot.send_message(
            chat_id=query.message.chat.id,
            text=f"❌ Erreur: {str(e)}"
        )
        print(f"Erreur callback: {str(e)}")


async def choisir_template(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🧾 Simple (ATS)", callback_data="template|ats")],
        [InlineKeyboardButton("🎯 Moderne", callback_data="template|Mod")],
        [InlineKeyboardButton("🎨 Créatif", callback_data="template|Crea")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("🧑‍🎓 Choisis un style de CV :", reply_markup=reply_markup)

async def template_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    _, template_choice = query.data.split("|")
    session = get_session(query.from_user.id)

    await query.edit_message_text("⚙️ Génération de ton CV en cours...")

    try:
        if template_choice == "Mod":
            file_path = session.moderne_cv()
        elif template_choice == "ats":
            file_path = session.simple_cv()
        elif template_choice == "Crea":
            file_path = session.creative_cv()
        else:
            raise Exception("❌ Modèle de CV inconnu.")

        with open(file_path, "rb") as file:
            await context.bot.send_document(
                chat_id=query.message.chat.id,
                document=InputFile(file),
                caption="✅ Voici ton CV prêt à l’emploi ! 🚀"
            )
    except Exception as e:
        await context.bot.send_message(
            chat_id=query.message.chat.id,
            text=f"❌ Une erreur est survenue : {e}"
        )
        print("Erreur template_callback:", e)

        
# fin

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

# =========================
# 📁 Flask pour Webhook Info
# =========================
nest_asyncio.apply()
flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "✅ Bot Telegram CV en ligne !"

# ============================
# 🌐 Commande /start et Menu Principal
# ============================
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

# ====================
# 🚧 Générateur de CV (PDF)
# ====================
async def generator(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Récupération de l'utilisateur et création d'une session s'il n'en a pas
    user = update.message.from_user
    user_id = user.id
    session = get_session(user_id)
    
    try:
        await update.message.reply_text("🛠️ Génération de ton CV en cours... ⏳")
        file_path = session.moderne_cv()
        with open(file_path, "rb") as file:
            await update.message.reply_document(
                document=InputFile(file),
                filename=os.path.basename(file_path),
                caption="✅ Voici ton CV tout beau, tout propre ! 💼\nTu peux le télécharger et l’utiliser directement."
            )
    except Exception as e:
        await update.message.reply_text(f"❌ Une erreur est survenue : {e}")
        print("Erreur :", e)



async def event_CVbuilding(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global session

    # Récupération de l'utilisateur et création d'une session s'il n'en a pas
    user = update.message.from_user
    user_id = user.id
    session = get_session(user_id)
    save_user(user)

    # Informer de l'étape actuelle (à des fins de debug)
    await update.message.reply_text(session.step)

    # 🧩 Partie 1 : L'entête (nom, prénom, ville, tel, email, lien)
    if session.step <= 5:
        if session.step == 0:
            await update.message.reply_text("Partie N° 1 : *l'entête 🪧*", parse_mode="Markdown")
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
            keyboard = [[KeyboardButton("Non fourni")]]
            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            await update.message.reply_text("Quel est le lien de ton compte LinkedIn ou ton site web ?", reply_markup=reply_markup)
            session.next_step()

    # 🧩 Étape 6 : Enregistrement du lien ou message par défaut
    elif session.step == 6:
        text = update.message.text
        keyboard = [[KeyboardButton("🧽 Clean")]]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

        if text == "Non fourni" or text == "Je n'en ai pas !!!":
            session.update_info("autre", "❌ Non fourni")
        else:
            session.update_info("autre", text)

        autre = session.data["autre"]
        await update.message.reply_text(header_summary(session.data, autre), reply_markup=reply_markup)

        await update.message.reply_text("Partie N° 2 : *le résumé 📜*", parse_mode="Markdown")
        await update.message.reply_text(text_conseil_resume, parse_mode="Markdown")
        await update.message.reply_text("Vas-y, écris ✍️")
        session.next_step()

    # 🧩 Étape 7 : Résumé personnel
    elif session.step == 7:
        session.update_info("resume", update.message.text)
        await update.message.reply_text(resume_summary(session.data), parse_mode="Markdown")
        await update.message.reply_text("Partie N° 3 : *Expérience professionnelle 🧑‍💼*", parse_mode="Markdown")
        await update.message.reply_text(text_conseil_Exp, parse_mode="Markdown")
        await update.message.reply_text("Combien d'expériences veux-tu ajouter ? (Ex: 1, 2, 3...)")
        session.next_step()

    # 🧩 Étapes 8 à 13 : Boucle d’ajout des expériences
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
        session.experiences.append(session.current_exp.copy())
        session.exp_index += 1

        if session.exp_index < session.nb_experiences:
            session.current_exp = {}
            await update.message.reply_text(f"👉 Expérience {session.exp_index + 1} : Quel est l’intitulé du poste ?")
            session.step = 9
        else:
            await update.message.reply_text("✅ Super, tu as terminé la section Expériences professionnelles !")
            session.next_step()  # step = 14
            await event_CVbuilding(update, context)

    # 🧩 Étape 14 : Résumé des expériences
    elif session.step == 14:
        await update.message.reply_text(str(len(session.experiences)))
        await update.message.reply_text(experience_summary(session.experiences), parse_mode="Markdown")
        session.next_step()
        await event_CVbuilding(update, context)

    # 🧩 Partie 4 : Formation académique
    elif session.step == 15:
        await update.message.reply_text("Partie N° 4 : *Formation 🎓*", parse_mode="Markdown")
        await update.message.reply_text(text_conseil_formation, parse_mode="Markdown")
        await update.message.reply_text("Combien de formations (diplômes ou certificats) veux-tu ajouter ? (ex : 2)")
        session.next_step()

    elif session.step == 16:
        try:
            session.nb_formations = int(update.message.text)
            session.format_index = 0
            session.current_format = {}
            await update.message.reply_text(f"👉 Formation {session.format_index + 1} : 1️⃣ Quel est l'intitulé du diplôme ou certificat ?")
            session.step = 17
        except ValueError:
            await update.message.reply_text("❌ Entre un nombre valide (1, 2, 3...)")

    elif session.step == 17:
        session.current_format["diplome"] = update.message.text
        await update.message.reply_text("2️⃣ Dans quel établissement l’as-tu obtenu ?")
        session.step = 18

    elif session.step == 18:
        session.current_format["etablissement"] = update.message.text
        await update.message.reply_text("3️⃣ Quelle est l’année de début ?")
        session.step = 19

    elif session.step == 19:
        session.current_format["date_debut"] = update.message.text
        await update.message.reply_text("4️⃣ Et l’année de fin ?")
        session.step = 20

    elif session.step == 20:
        session.current_format["date_fin"] = update.message.text
        await update.message.reply_text("Enfin le lieu ?")
        session.step = 21

    elif session.step == 21:
        session.current_format["lieu"] = update.message.text
        session.formations.append(session.current_format.copy())
        session.format_index += 1

        if session.format_index < session.nb_formations:
            session.current_format = {}
            await update.message.reply_text(f"👉 Formation {session.format_index + 1} : 1️⃣ Quel est l'intitulé du diplôme ou certificat ?")
            session.step = 17
        else:
            await update.message.reply_text("✅ Super, tu as terminé la section Formation !")
            session.next_step()
            await event_CVbuilding(update, context)

    # 🧩 Étape 22 : Résumé des formations + transition
    elif session.step == 22:
        await update.message.reply_text(education_summary(session.formations), parse_mode="Markdown")
        await update.message.reply_text("Partie N° 5: *Compétences 🧰*", parse_mode="Markdown")
        await update.message.reply_text(competence_conseil, parse_mode="Markdown")
        await update.message.reply_text("Combien de compétences maîtrises-tu ?")
        session.next_step()

    # 🧩 Étapes 23-24 : Compétences
    elif session.step == 23:
        try:
            session.nb_comp = int(update.message.text)
            session.comp_index = 0
            session.current_comp = {}
            await update.message.reply_text(f"👉 Compétence {session.comp_index + 1} : Quel est cette compétence ?")
            session.step = 24
        except ValueError:
            await update.message.reply_text("❌ Entre un nombre valide (1, 2, 3...)")

    elif session.step == 24:
        session.current_comp["comp"] = update.message.text
        session.competences.append(session.current_comp.copy())
        session.comp_index += 1

        if session.comp_index < session.nb_comp:
            session.current_comp = {}
            await update.message.reply_text(f"👉 Compétence {session.comp_index + 1} : Quel est cette compétence ?")
        else:
            await update.message.reply_text("✅ Super, tu as terminé la section compétences !")
            session.step = 26
            await event_CVbuilding(update, context)

    # 🧩 Étapes 26-28 : Langues
    elif session.step == 26:
        await update.message.reply_text(skills_summary(session.competences), parse_mode="Markdown")
        await update.message.reply_text("Partie N° 6: *Langues 🗣️*", parse_mode="Markdown")
        await update.message.reply_text("Combien de langues maîtrises-tu ?")
        session.next_step()

    elif session.step == 27:
        try:
            session.nb_lag = int(update.message.text)
            session.lag_index = 0
            session.current_lag = {}
            await update.message.reply_text(f"👉 Langue {session.lag_index + 1} : Quel est le nom de la langue ?")
            session.step = 28
        except ValueError:
            await update.message.reply_text("❌ Entre un nombre valide (1, 2, 3...)")

    elif session.step == 28:
        session.current_lag["nom"] = update.message.text
        session.langues.append(session.current_lag.copy())
        session.lag_index += 1

        if session.lag_index < session.nb_lag:
            session.current_lag = {}
            await update.message.reply_text(f"👉 Langue {session.lag_index + 1} : Quel est le nom de la langue ?")
        else:
            await update.message.reply_text("✅ Super, tu as terminé la section Langues !")
            session.step = 29
            await event_CVbuilding(update, context)

    # 🧾 Étape 29 : Génération du CV final
    elif session.step == 29:
        choisir_template()


# ====================
# 📊 Gestion des messages
# ====================
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.message.from_user.id
    session = get_session(user_id)

    if text == "📝 Créer un CV":
        session.step = 0
        await update.message.reply_text("Super ! Commençons la création du CV.")
        await event_CVbuilding(update, context)

    elif text == "📄 Voir un exemple":
        await update.message.reply_text("Voici un exemple de CV:")
        await see_modele()

    elif text == "⚙️ Aide":
        await update.message.reply_text(texte_aide, parse_mode="Markdown")
        await infos(update, context)

    elif text == "❌ Quitter":
        await update.message.reply_text("Merci et à bientôt !")

    elif text == "🧽 Clean":
        if user_id in sessions:
            del sessions[user_id]
        await update.message.reply_text("Données utilisateur réinitialisées.", reply_markup=ReplyKeyboardMarkup([
            [KeyboardButton("📝 Créer un CV"), KeyboardButton("📄 Voir un exemple")],
            [KeyboardButton("⚙️ Aide"), KeyboardButton("❌ Quitter")],
            [KeyboardButton("🧽 Clean")]
        ], resize_keyboard=True))

    else:
        if session.step >= 1:
            await event_CVbuilding(update, context)
        else:
            await update.message.reply_text("Commande non reconnue. Choisis un bouton dans le menu.")

# ======================
# 🎓 Lancement du bot + Webhook
# ======================
async def run():
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("sendusers", send_users_command))
    app.add_handler(CommandHandler("id", get_id_command))
    app.add_handler(CommandHandler("gr", generator))
    #app.add_handler(CommandHandler("test", test_modern_cv_generator))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CommandHandler("voir_modeles", see_modele))
    app.add_handler(CallbackQueryHandler(modele_callback))
    app.add_handler(CommandHandler("generer", choisir_template))
    app.add_handler(CallbackQueryHandler(template_callback, pattern="^template\|"))

    await app.initialize()
    await app.start()
    await app.updater.start_polling()

    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, lambda: flask_app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000))))

# ======================
# ⭐ Point d'entrée du script
# ======================
if __name__ == '__main__':
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    keep_alive(token, CHANNEL_ID)
    asyncio.get_event_loop().run_until_complete(run())
    
