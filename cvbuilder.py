class CVBuilder:
    def __init__(self):
        self.step = 0
        self.data = {
            "prenom": "",
            "nom": "",
            "email": "",
            "tel": "",
            "autre": "",
            "resume": ""
        }
        self.competences = []
        self.current_comp = {}  # Temporaire
        self.comp_index = 0     # Quelle expérience on est en train de saisir
        self.nb_comp = 0
        
        self.experiences = []  # Liste pour stocker plusieurs expériences
        self.current_exp = {}  # Temporaire
        self.exp_index = 0     # Quelle expérience on est en train de saisir
        self.nb_experiences = 0
        
        self.formations = []
        self.current_format = {}  # Temporaire
        self.format_index = 0     # Quelle formation on est en train de saisir
        self.nb_formations = 0

        self.langues = []
        self.current_lag = {}  # Temporaire
        self.lag_index = 0     # Quelle formation on est en train de saisir
        self.nb_lag = 0
        

    def next_step(self):
        self.step += 1

    def update_info(self, key, value):
        self.data[key] = value

    def simple_cv(self):
        from telegram import InputFile
        from jinja2 import Environment, FileSystemLoader
        from weasyprint import HTML
        import os

        # Charger le template depuis le dossier Template/ATS
        env = Environment(loader=FileSystemLoader('Template/ATS'))
        template = env.get_template('ats_template.html')

        # Organisation des données pour le template
        context = {
        "infos": self.data,
        "experiences": self.experiences,
        "competences": self.competences,
        "formations": self.formations,
        "langues": self.langues
        }

        # Rendu HTML du template
        html = template.render(context)

        # Nom de fichier sécurisé
        nom = self.data.get('nom', 'cv').replace(" ", "_").lower()
        nom_fichier = f"{nom}_ats.pdf"

        # Chemin de sauvegarde (optionnel : créer un dossier "generated_cv")
        dossier = "generated_cv"
        os.makedirs(dossier, exist_ok=True)
        chemin_complet = os.path.join(dossier, nom_fichier)

        # Génération du PDF
        HTML(string=html, base_url='Template/ATS').write_pdf(chemin_complet)

        return chemin_complet
