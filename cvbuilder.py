class CVBuilder:
    def __init__(self):
        self.step = 0
        self.data = {
            "prenom": "",
            "nom": "",
            "email": "",
            "tel": "",
            "autre": "",
            "resume": "",
            "competences": [],
            "experiences": [],
            "formations": []
        }

    def next_step(self):
        self.step += 1

    def update_data(self, key, value):
        self.data[key] = value
