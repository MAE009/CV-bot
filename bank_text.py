
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
            texte += f"🔹 {i+1}. {skill.get("comp", '')}\n"
    texte += "\n✅ *Conseil* : Ne liste que les compétences que tu maîtrises vraiment. Mieux vaut peu mais solide 💪"
    return texte
    

def langues_summary(langues):
    texte_lag = "📌 *Récapitulatif - Langues* \n"
    for i, lag in enumerate(langues):
        texte_lag += (
            f"{i+1} : 🗣️ {lag.get('nom', '')}\n"
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


test_data = {
    "infos": {
        "nom": "DUPONT",
        "prenom": "Jean",
        "poste": "Développeur Python Senior",
        "ville": "Paris, France",
        "tel": "+33 6 12 34 56 78",
        "email": "j.dupont@email.com",
        "autre": "https://linkedin.com/in/jdupont",
        "resume": (
            "Développeur Python avec 5+ ans d'expérience dans le développement backend "
            "et l'analyse de données. Expert en Django, Flask et Pandas. Passionné par "
            "l'optimisation des performances et les architectures microservices."
        )
    },
    "experiences": [
        {
            "poste": "Développeur Backend Senior",
            "entreprise": "TechCorp",
            "date": "2020 - Présent",
            "description": "Conception d'APIs RESTful pour une plateforme SaaS avec Django.",
            "realisations": (
                "Migration réussie vers Kubernetes, amélioration des temps de réponse de 40%."
            )
        },
        {
            "poste": "Développeur Python",
            "entreprise": "DataSystems",
            "date": "2018 - 2020",
            "description": "Développement de scripts ETL pour le traitement de données clients.",
            "realisations": (
                "Automatisation de rapports mensuels économisant 20h/mois."
            )
        }
    ],
    "formations": [
        {
            "diplome": "Master en Informatique",
            "etablissement": "Université Paris-Saclay",
            "date_debut": "2016",
            "date_fin": "2018",
            "lieu": "Paris"
        },
        {
            "diplome": "Licence en Mathématiques Appliquées",
            "etablissement": "Sorbonne Université",
            "date_debut": "2013",
            "date_fin": "2016",
            "lieu": "Paris"
        }
    ],
    "competences": [
        {"comp": "Python (Django, Flask)"},
        {"comp": "SQL/NoSQL"},
        {"comp": "Docker/Kubernetes"},
        {"comp": "Pandas/Numpy"}
    ],
    "langues": [
        {"nom": "Français (Langue maternelle)"},
        {"nom": "Anglais (Courant - TOEFL 950)"}
    ]
}


test_data_maman = {        
    "infos": {        
        "nom": "MAKOSSO PAMBOU",        
        "prenom": "Edith Chantal",        
        "poste": "Agent de service cantine scolaire",        
        "ville": "POINTE-NOIRE, Siafoumou",        
        "tel": "+242 064118105",        
        "email": "❌ Non fourni",        
        "autre": "❌ Non fourni",        
        "resume": (        
            "Expérimentée dans le service en cantine scolaire et la préparation des repas collectifs. "
            "Sérieuse, organisée et attentive au respect des règles d'hygiène, avec un bon relationnel "
            "auprès des enfants et de l'équipe."        
        )        
    },        

    "experiences": [        
        {        
            "poste": "Gérante",        
            "entreprise": "Mon restaurant local",        
            "date": "2016 - 2019",        
            "description": "Préparation et vente de repas variés à une clientèle locale.",        
            "realisations": (        
                "Restauration rapide"        
            )        
        },
        {        
            "poste": "Cantinière",        
            "entreprise": "Complexe scolaire La Croyance",        
            "date": "Octobre 2012 - Juin 2013",        
            "description": "Service des repas et encadrement des enfants en cantine et Mise en place de plats traditionnels (Bissa, yaourt, gâteaux) appréciés par les enfants.",        
            "realisations": (        
                "Assurer une distribution fluide et respectueuse des règles d'hygiène."        
            )        
        },        
        {        
            "poste": "Cantinière",        
            "entreprise": "École Fanoe",        
            "date": "Septembre 2009 - Mars 2011",        
            "description": "Préparation et service des repas scolaires.",        
            "realisations": (        
                "Soutien à la discipline et au bon déroulement des repas des enfants."        
            )        
        }        
    ],        

    "formations": [        
        {        
            "diplome": "BTS en Secrétariat",        
            "etablissement": "ESC",        
            "date_debut": "2001",        
            "date_fin": "2003",        
            "lieu": "Congo"        
        },        
        {        
            "diplome": "Baccalauréat",        
            "etablissement": "Poaty Bernard",        
            "date_debut": "1999",        
            "date_fin": "2001",        
            "lieu": "Congo"        
        }        
    ],        

    "competences": [        
        {"comp": "Service en cantine,"},        
        {"comp": "Préparation des repas,"},        
        {"comp": "Hygiène,"},        
        {"comp": "Travail en équipe,"},        
        {"comp": "Relationnel avec enfants,"},        
        {"comp": "Préparation Bissa, yaourt et gâteaux"}        
    ],        

    "langues": [        
        {"nom": "Français (langue maternelle)"}        
    ],
    "photo_path" : "Assets/1756384517199.jpg"
}

test_data_duc = {        
    "infos": {        
        "nom": "MAKOSSO",        
        "prenom": "Ducerne Dieu-merci",        
        "poste": "Étudiant en génie industriel et maintenance",        
        "ville": "Pointe-Noire, Congo Brazzaville",        
        "tel": "+242 068620127",        
        "email": "makossoducerne@gmail.com",        
        "autre": "Lien LinkedIn : Oui",        
        "resume": (        
            "Étudiant motivé en génie industriel et maintenance, avec une expérience en milieu professionnel "
            "acquise au sein de DGC Congo. Passionné par la maintenance corrective et préventive, "
            "le suivi technique des équipements, et doté de bases solides en conception et analyse technique."
        )        
    },        

    "experiences": [        
        {        
            "poste": "Stagiaire en génie industriel et maintenance",        
            "entreprise": "DGC Congo",        
            "date": "Octobre - Novembre 2025",        
            "description": "Découverte et participation aux activités de maintenance corrective et préventive, suivi technique des équipements et apprentissage en milieu professionnel.",        
            "realisations": (        
                "Réalisation d’un projet tutoré portant sur l’étude de l’installation électrique d’un bâtiment à usage hôtelier R+1."        
            )        
        }        
    ],        

    "formations": [        
        {        
            "diplome": "Baccalauréat",        
            "etablissement": "L’Alpha",        
            "date_debut": "2022",        
            "date_fin": "2023",        
            "lieu": "Tchiali"        
        },        
        {        
            "diplome": "BEPC",        
            "etablissement": "L’Alpha",        
            "date_debut": "2019",        
            "date_fin": "2020",        
            "lieu": "Tchiali"        
        }        
    ],        

    "competences": [        
        {"comp": "SolidWorks"},        
        {"comp": "AMDEC"},        
        {"comp": "Word"}        
    ],        

    "langues": [        
        {"nom": "Français (natif)"},        
        {"nom": "Anglais"}        
    ],    

    "photo_path" : "Assets/Ducerne.jpg"  # À remplacer par ton vrai chemin d'image
}





test_data_emmanuel = {
    "infos": {
        "nom": "MAYALA",
        "prenom": "Armand Emmanuel",  # à remplir
        "poste": "Étudiant en Génie Industriel et Maintenance",
        "ville": "Pointe-Noire, Congo Brazzaville",
        "tel": "+242 065628783",  # en attente
        "email": "emmanuelmayala40@gmail.com",  # si tu veux l’ajouter
        "autre": "https://www.linkedin.com/in/emmanuel-mayala",
        "resume": (
            "Étudiant motivé en génie industriel et maintenance, passionné par le froid industriel, "
            "l’électricité, la mécanique et l’optimisation des systèmes. "
            "Actuellement en stage à la Congolaise de Congélation (LCC), où je participe aux interventions "
            "de maintenance préventive et corrective sur les chambres froides, les groupes électrogènes, "
            "les climatiseurs et les véhicules industriels. Je développe également des outils en VBA "
            "pour automatiser et améliorer la gestion des rapports de maintenance."
        )
    },

    "experiences": [
        {
            "poste": "Stagiaire Maintenance Industrielle",
            "entreprise": "La Congolaise de Congélation (LCC)",
            "date": "Octobre - Décembre 2025",
            "description": (
                "Participation aux activités de maintenance des équipements frigorifiques, "
                "électriques et mécaniques ; réalisation d'interventions préventives et curatives ; "
                "travail en hauteur, dépannages et diagnostics sur groupes électrogènes et circuits électriques."
            ),
            "realisations": (
                "Développement d'une macro VBA pour consolider automatiquement les rapports journaliers ; "
                "entretien de climatiseurs et chambres froides ; dépannage d’inverseurs, disjoncteurs et luminaires ; "
                "vidange et entretien de groupes électrogènes Caterpillar ; interventions sur poids lourds et légers."
            )
        }

    ],

    "formations": [
        {
            "diplome": "Licence 2 — Génie Industriel et Maintenance",
            "etablissement": "Université DGC Congo",
            "date_debut": "2024",
            "date_fin": "2025",
            "lieu": "Pointe-Noire"
        },
        {
            "diplome": "Baccalauréat",
            "etablissement": "L’établissement que tu me donneras",
            "date_debut": "année",
            "date_fin": "année",
            "lieu": "lieu"
        }
    ],

    "competences": [
        {"comp": "Maintenance Industrielle"},
        {"comp": "Froid Industriel"},
        {"comp": "Électricité Industrielle"},
        {"comp": "Mécanique Automobile"},
        {"comp": "Groupes électrogènes"},
        {"comp": "VBA / Excel avancé"},
        {"comp": "AMDEC"},
        {"comp": "Gestion de stock"},
        {"comp": "Automatisation de macros"},
        {"comp": "Thermodynamique"}
    ],

    "langues": [
        {"nom": "Français (natif)"},
        {"nom": "Anglais (notions professionnelles)"}
    ],

    "photo_path": "Assets/Ducerne.jpg"  # en attente
}

test_data_betina = {
    "infos": {
        "nom": "BOSSOTA BOMBAKA",
        "prenom": "Betina Exaucé",
        "poste": "Assistante commerciale junior",
        "ville": "Brazzaville, Congo",
        "tel": "+242 066585742",
        "email": "callmebeetina@gmail.com",
        "autre": "https://www.linkedin.com/in/betina-exauc%C3%A9-bossota-bombaka-8ba706392",
        "resume": (
            "Assistante commerciale rigoureuse et orientée résultats, avec une solide expérience en prospection, "
            "gestion administrative, suivi commercial et relation client. À l'aise dans la communication, la coordination "
            "et la gestion des priorités, j'assure un soutien efficace aux équipes commerciales tout en veillant à la satisfaction client. "
            "Je maîtrise les techniques de vente, la gestion de portefeuille, les relances professionnelles et l'organisation administrative."
        )
    },

    "experiences": [
        {
            "poste": "Assistante de Direction (Intérim)",
            "entreprise": "Société de Promotion Immobilière",
            "date": "Août - Décembre 2023",
            "description": "Gestion des appels entrants, organisation des réunions et suivi des dossiers. Accueil, orientation et prise en charge des demandes clients. Support administratif à la direction et coordination interne.",
            "realisations": (
                "Rédaction, mise en forme et gestion documentaire."
            )
        },
        {
            "poste": "Agent de Recouvrement",
            "entreprise": "Société de Promotion Immobilière",
            "date": "Août - Décembre 2023",
            "description": "Gestion d'un portefeuille clients et suivi des créances. Relances téléphoniques et mails professionnels. Négociation d'échéanciers et gestion des litiges.",
            "realisations": (
                "Reporting précis et amélioration du taux de recouvrement."
            )
        },
        {
            "poste": "Assistante Commerciale & Marketing (Stage)",
            "entreprise": "Société de Promotion Immobilière",
            "date": "Août - Décembre 2023",
            "description": "Prospection commerciale, qualification des contacts et suivi des leads. Préparation des offres commerciales et participation aux actions marketing. Suivi client, analyse des besoins et mise à jour du CRM.",
            "realisations": (
                "Support aux commerciaux : organisation, documentation, reporting."
            )
        },
        {
            "poste": "Agent Commercial",
            "entreprise": "1er Bet",
            "date": "Non précisé",
            "description": "Prospection terrain et présentation des offres. Acquisition de nouveaux clients et ventes directes. Argumentaires commerciaux et gestion des objections.",
            "realisations": (
                "Contribution à l'augmentation du chiffre d'affaires."
            )
        }
    ],

    "formations": [
        {
            "diplome": "Brevet de Technicien Supérieur",
            "etablissement": "ESGAE (École Supérieure de Gestion et d'administration des Entreprises)",
            "date_debut": "2021",
            "date_fin": "2023",
            "lieu": "Brazzaville"
        }
    ],

    "competences": [
        {"comp": "Gestion administrative & commerciale 📊"},
        {"comp": "Prospection et qualification de leads 🔍"},
        {"comp": "Suivi des clients & reporting 📈"},
        {"comp": "Recouvrement & relances professionnelles 💼"},
        {"comp": "Gestion d'agendas, réunions & appels entrants 📅"},
        {"comp": "Préparation de dossiers commerciaux 📑"},
        {"comp": "Communication professionnelle 💬"},
        {"comp": "Organisation, rigueur, sens du détail ✅"},
        {"comp": "Gestion des objections & support aux commerciaux 🤝"},
        {"comp": "Service client & fidélisation 💎"}
    ],

    "langues": [
        {"nom": "Français (courant) 🇫🇷"},
        {"nom": "Lingala 🇨🇬"},
        {"nom": "Anglais (débutant) 🇬🇧"}
    ],

    #"informatique": [
      #  {"outil": "Pack Office 📁"},
     #   {"outil": "Excel 📊"},
    #    {"outil": "Google Workspace ☁️"},
    #    {"outil": "CRM 💻"},
    #    {"outil": "Outils de suivi & reporting 📈"}
  #  ],
    
    "photo_path": None  # À remplacer par le chemin de la photo si disponible
}
