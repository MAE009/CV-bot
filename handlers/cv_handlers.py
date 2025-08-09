import os
from telegram import (
    Update, ReplyKeyboardMarkup, KeyboardButton, InputFile,
    InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
)
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters, CallbackQueryHandler
)
from cvbuilder import CVBuilder
from utils.helpers import *
from user import *
from bank_text import *  # Textes prédéfinis (conseils, résumés...)




"""
async def choisir_template(update: Update, context: ContextTypes.DEFAULT_TYPE):
    #Affiche le menu de sélection de template
    buttons = [
        KeyboardButton("🧾 Simple (ATS)"),
        KeyboardButton("🎯 Moderne"),
        KeyboardButton("🎨 Créatif"),
        KeyboardButton("❌ Annuler")
    ]
    # Organisez en 2 colonnes
    keyboard = [buttons[i:i+2] for i in range(0, len(buttons), 2)]
    
    reply_markup = ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        one_time_keyboard=True  # Le clavier disparaît après sélection
    )
    
    await update.message.reply_text(
        "🧑‍🎓 Choisis un style de CV :",
        reply_markup=reply_markup
    )



async def generator(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Récupération de l'utilisateur et création d'une session s'il n'en a pas
    user = update.message.from_user
    user_id = user.id
    session = get_session(user_id)
   # await choisir_template()
    choix = update.message.text
    await update.message.reply_text(choix)

    
    
    try:
        
        await update.message.reply_text("🛠️ Génération de ton CV en cours... ⏳")
        #
        if "Simple" in choix:
            file_path = session.simple_cv()
        elif "Moderne" in choix :
            file_path = session.moderne_cv()
        elif "Créatif" in choix:
            file_path = session.creative_cv()
        else:
            raise ValueError("Choix non reconnu")
        #
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


from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, InputFile, ReplyKeyboardRemove
from telegram.ext import ContextTypes, MessageHandler, filters
from cvbuilder import CVBuilder
"""

# Fonction pour choisir le template
async def choisir_template(update: Update, context: ContextTypes.DEFAULT_TYPE):
    #Affiche le menu de sélection de template
    buttons = [
        KeyboardButton("🧾 Simple (ATS)"),
        KeyboardButton("🎯 Moderne"), 
        KeyboardButton("🎨 Créatif"),
        KeyboardButton("❌ Annuler")
    ]
    keyboard = [buttons[i:i+2] for i in range(0, len(buttons), 2)]
    
    # Configure l'attente du choix
    session = get_session(update.message.from_user.id)
    session.waiting_for = "template_choice"
    
    await update.message.reply_text(
        "🧑‍🎓 Choisis un style de CV :",
        reply_markup=ReplyKeyboardMarkup(
            keyboard,
            resize_keyboard=True,
            one_time_keyboard=True
        )
    )

# Fonction pour générer le CV
async def generate_cv(update: Update, context: ContextTypes.DEFAULT_TYPE):
    #Génère le CV selon le template choisi
    choice = update.message.text
    session = get_session(update.message.from_user.id)
    
    try:
        await update.message.reply_text(
            f"🛠️ Génération du CV {choice} en cours...",
            reply_markup=ReplyKeyboardRemove()
        )
        
        if "Simple" in choice:
            file_path = session.simple_cv()
            template_name = "Simple (ATS)"
        elif "Moderne" in choice:
            file_path = session.moderne_cv() 
            template_name = "Moderne"
        elif "Créatif" in choice:
            file_path = session.creative_cv()
            template_name = "Créatif"
        elif "Annuler" in choice:
            await update.message.reply_text("❌ Génération annulée")
            return
        else:
            raise ValueError("Type de template inconnu")

        # Envoi du CV généré
        with open(file_path, "rb") as f:
            await update.message.reply_document(
                document=InputFile(f),
                filename=f"CV_{template_name}.pdf",
                caption=f"✅ Ton CV {template_name} est prêt !"
            )
            
    except Exception as e:
        await update.message.reply_text(f"❌ Erreur: {str(e)}")
        print(f"Erreur génération: {str(e)}")

# Handler principal
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    #Route les messages vers la bonne fonction
    session = get_session(update.message.from_user.id)
    
    # Si on attend un choix de template
    if getattr(session, 'waiting_for', None) == "template_choice":
        session.waiting_for = None
        await generate_cv(update, context)
        return
        
    # Sinon poursuit le processus normal
    await event_CVbuilding(update, context)

# Configuration des handlers
#def setup_handlers(app):
   # app.add_handler(MessageHandler(
        #filters.TEXT & filters.Regex(r"^(🧾 Simple \(ATS\)|🎯 Moderne|🎨 Créatif|❌ Annuler)$"),
        #handle_message
   # ))




def setup_cv_handlers(app):
    app.add_handler(CommandHandler("cv", choisir_template))
   # app.add_handler(MessageHandler(
        #filters.TEXT & filters.Regex(r"^(🧾 Simple \(ATS\)|🎯 Moderne|🎨 Créatif|❌ Annuler)$"),
       # handle_message
    #))
    #app.add_handler(CommandHandler("gr", generator))
    # Autres handlers CV...




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
