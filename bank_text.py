
# bank_text.py

def header_summary(data, autre):
    return (
        f"🧾 En-tête :\n"
        f"👤 {data['nom']} {data['prenom']}\n"
        f"📍 {data['ville']} || "
        f"📞 {data['tel']} || 📧 {data['email']}\n"
        f"🔗 {autre}"
    )

def resume_summary(data):
    return (
        "🎯 Résumé Professionnel\n"
        f"{"="*30}\n"
        f"{data["resume"]}\n"
        f"{"="*30}\n\n"   
        "✅ *Conseil* : Ce résumé est souvent la première chose lue par un recruteur. Sois clair, concis, et montre ce que tu veux faire !"
    )

def experience_summary(experiences):
    texte_exp = "📌 *Récapitulatif - Expériences professionnelles* \n"
    for i, exp in enumerate(experiences):
        texte_exp += (
            f"\n🧪 Expérience {i+1} :\n"
            f"🧑 Poste : {exp.get('poste', '')}\n"
            f"🏢 Entreprise : {exp.get('entreprise', '')}\n"
            f"📅 Dates : {exp.get('date', '')}\n"
            f"📝 Fonctions : {exp.get('description', '')}\n"
            f"🎯 Réalisations : {exp.get('realisations', '')}\n"
        )
    texte_exp += "\n✅ *Conseil* : Commence toujours par l’expérience la plus récente. Sois précis et n’exagère pas 😉"
    return texte_exp



def education_summary(educations):
    texte_edu = "📌 *Récapitulatif - Formations* \n"
    for i, edu in enumerate(educations):
        texte_edu += (
            f"\n🎓 Formation {i+1} :\n"
            f"🏫 Établissement : {edu.get('établissement', '')}\n"
            f"📘 Diplôme : {edu.get('diplôme', '')}\n"
            f"📅 Années : {edu.get('date_debut', '')} - {edu.get('date_fin', '')}\n"
            f"📍 Lieu : {edu.get('lieu', '')}\n"
        )
    texte_edu += "\n✅ *Conseil* : Mets en avant les diplômes les plus pertinents pour le poste visé. Mentionne l’année d’obtention clairement."
    return texte_edu


def skills_summary(skills_list):
    texte = "📌 *Récapitulatif - Compétences* \n\n"
    if not skills_list:
        texte += "Aucune compétence enregistrée."
    else:
        for i, skill in enumerate(skills_list):
            texte += f"🔹 {i+1}. {skill}\n"
    texte += "\n✅ *Conseil* : Ne liste que les compétences que tu maîtrises vraiment. Mieux vaut peu mais solide 💪"
    return texte
    

def langues_summary(langues):
    texte_lag = "📌 *Récapitulatif - Langues* \n"
    for i, lag in enumerate(langues):
        texte_lag += (
            f"{i} : 🗣️ {lag.get('nom', '')}\n"
        )
    return texte_lag




competence_conseil = (
    "✅ *Conseil - Compétences*\n\n"
    "🧠 La rubrique *Compétences*, c’est un peu ta carte Pokémon : montre ce que tu sais faire, ce que tu maîtrises, et ce qui te rend unique 💥\n\n"
    "📌 C’est grâce à elle que ton CV passe les robots ATS (oui, ces recruteurs robots qui scannent les CV 👾). Mets-y les bons mots-clés sinon... *GAME OVER* 🎮\n\n"
    "🔑 Astuce : sélectionne entre *8 à 15 compétences* pertinentes. Pas besoin de tout mettre, on veut le meilleur, pas l’inventaire de ton cerveau 🧰🧠.\n\n"
    "💡 Et surtout, *adapte tes compétences à chaque offre* d’emploi ! Un bon CV, c’est comme un bon plat : ça se prépare sur-mesure 🍽️😉"
)



text_conseil_formation = """
🎓 *Conseil – Formation*

La section *Formation*, c’est un peu la carte d’identité scolaire de ton CV 🎒. Elle montre que tu n’es pas tombé dans la marmite de la compétence par hasard, mais que tu as bossé dur pour en arriver là 📚💪.

✅ Elle doit inclure :
- 🎓 Le(s) diplôme(s) obtenu(s)
- 🏫 L’établissement fréquenté
- 📅 Les années de début et de fin (oui, les deux, pas juste "2020"... c’est louche sinon 👀)

🧠 Et surtout : classe-les dans l’ordre **chronologique décroissant** ! Commence toujours par ta dernière formation (la plus récente = la plus pertinente 🧲).  
Faire l’inverse, c’est comme lire la fin d’un manga avant le début : c’est bizarre et personne ne fait ça (sauf peut-être les méchants 😈).

📌 Pourquoi c’est important ?  
Parce que les recruteurs veulent voir immédiatement ta dernière étape de formation. C’est ce qui leur donne une idée de *ce que tu sais aujourd’hui*, pas de ce que tu as appris au collège ✏️.

⚠️ Petit rappel (parce que c’est courant) : n’oublie pas les dates ! Une formation sans date, c’est comme un diplôme dans une chaussette… On ne sait pas trop d’où ça sort 🧦🎭. Et crois-moi, les recruteurs ont un détecteur de flou artistique activé en permanence !

🎯 Alors fais en sorte que ta section Formation soit claire, complète et bien classée. C’est l’occasion de montrer que tu as de la matière grise, et que tu sais aussi la présenter avec style 😎.
"""



    
text_conseil_Exp = """
🎯 *Conseil – Expérience Professionnelle*

Ta section "Expérience professionnelle" ? C’est le cœur de ton CV ❤️‍🔥 ! Elle montre clairement ce que tu sais faire, où tu l’as fait, et ce que tu as accompli. C’est là que les recruteurs vont chercher *la preuve* que tu es la bonne personne pour le poste. Alors… ne la bâcle pas 😏.

✅ *Assure-toi d’indiquer :*
- 🧑‍💼 Le poste occupé
- 🏢 Le nom de l’entreprise
- 🗓️ Les dates (mois + année, hein ! Pas juste “2021–2023” 🙃)
- 🛠️ Une brève description de tes missions
- 🌟 Tes réalisations concrètes

💡 Pro-tip : Liste toujours tes expériences en ordre chronologique *décroissant* (la plus récente en premier). Pourquoi ? Parce que les recruteurs veulent savoir ce que tu fais *en ce moment* ou ce que tu as fait dernièrement – pas ce que tu faisais au lycée 😅

⚠️ Attention ! N'oublie pas les dates de début ou de fin. C’est un peu comme regarder un film sans savoir quand il commence ni quand il finit 🎬... Frustrant !

📈 Bref : montre ta progression, sois clair, précis, et évite d’en faire trop. On veut du concret, pas une biographie de super-héros (à moins que tu sois Batman, là c’est différent 🦇).
"""



text_conseil_resume = """🎯 *Petit conseil pour booster ton CV !*

Tu n’as pas encore ajouté de résumé professionnel ? C’est dommage, car c’est souvent la première chose que les recruteurs lisent 👀.

💡 En 2-3 phrases (environ 50 à 100 mots), tu peux :
✅ Mettre en avant tes compétences clés
✅ Résumer ton expérience
✅ Montrer tes objectifs ou ambitions pro

Pense à cette section comme une pub express de toi-même 📣 — elle peut vraiment te faire sortir du lot ✨. Alors n’hésite pas à la rédiger pour capter l’attention en quelques secondes !
"""

texte_aide = """
🛠️ *Aide - Que fait chaque bouton ?*

Voici les fonctionnalités disponibles :

📝 *Créer un CV*  
➡️ Lance la création de ton CV étape par étape. Je te poserai des questions simples (nom, email, compétences, etc.) pour construire ton CV personnalisé.

📄 *Voir un exemple*  
➡️ Affiche un exemple de CV fictif pour t’inspirer.

⚙️ *Aide*  
➡️ Affiche ce message pour t’expliquer à quoi servent tous les boutons du menu.

❌ *Quitter*  
➡️ Termine la session actuelle. Tu peux revenir à tout moment en tapant /start.

🧽 *Clean*  
➡️ Réinitialise toutes tes données enregistrées. À utiliser si tu veux recommencer un nouveau CV depuis zéro.

ℹ️ *Et après ?*  
Une fois le CV terminé, il sera généré automatiquement et tu pourras le télécharger au format Word ou PDF.

Besoin d’aide ? Tu peux toujours me taper `/start` pour revenir au menu principal.
"""
