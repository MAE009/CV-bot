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
        self.nb_langues = 0
        

    def next_step(self):
        self.step += 1

    def update_info(self, key, value):
        self.data[key] = value
