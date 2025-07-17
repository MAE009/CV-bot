
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

⚠️ Attention ! N'oubliez pas les dates de début ou de fin. C’est un peu comme regarder un film sans savoir quand il commence ni quand il finit 🎬... Frustrant !

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
