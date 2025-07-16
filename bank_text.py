
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
        "📌 *Récapitulatif - Résumé professionnel* \n"
        f"{'='*50}\n"
        f"{data.get('resume', 'Pas encore fourni.')}\n"
        f"{'='*50}\n\n"
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
