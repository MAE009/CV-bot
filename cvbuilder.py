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

        env = Environment(loader=FileSystemLoader('Template/ATS'))
        template = env.get_template('ats_template.html')

        # Organisation des données à injecter dans le template
        context = {
            "infos": self.data,
            "experiences": self.experiences,
            "competences": self.competences,
            "formations": self.formations,
            "langues": self.langues
        }

        html = template.render(context)
    
        # Nom de fichier sécurisé
        nom_fichier = f"{self.data.get('nom', 'cv')}_ats.pdf"
        HTML(string=html, base_url='.').write_pdf(nom_fichier)
