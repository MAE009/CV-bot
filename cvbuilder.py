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
        self.current_comp = {}  
        self.comp_index = 0  
        self.nb_comp = 0  
        
        self.experiences = []  
        self.current_exp = {}  
        self.exp_index = 0  
        self.nb_experiences = 0  
        
        self.formations = []  
        self.current_format = {}  
        self.format_index = 0  
        self.nb_formations = 0  

        self.langues = []  
        self.current_lag = {}  
        self.lag_index = 0  
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

        env = Environment(loader=FileSystemLoader('Template/ATS'))  
        template = env.get_template('ats.html')  

        context = {  
            "infos": self.data,  
            "experiences": self.experiences,  
            "competences": self.competences,  
            "formations": self.formations,  
            "langues": self.langues  
        }  

        html = template.render(context)  

        nom = self.data.get('nom', 'cv').replace(" ", "_").lower()  
        nom_fichier = f"{nom}_ats.pdf"  

        dossier = "generated_cv"  
        os.makedirs(dossier, exist_ok=True)  
        chemin_complet = os.path.join(dossier, nom_fichier)  

        HTML(string=html, base_url='Template/ATS').write_pdf(chemin_complet)  

        return chemin_complet  

    def moderne_cv(self):  
        from telegram import InputFile  
        from jinja2 import Environment, FileSystemLoader  
        from weasyprint import HTML  
        import os  

        env = Environment(loader=FileSystemLoader('Template/Moderne'))  
        template = env.get_template('Mod.html')  

        total_chars = sum(len(v) for v in self.data.values())  
        total_chars += sum(len(exp.get("description", "")) for exp in self.experiences)  
        total_chars += sum(len(comp.get("description", "")) for comp in self.competences)  
        total_chars += sum(len(form.get("diplome", "")) for form in self.formations)  
        total_chars += sum(len(lang.get("nom", "")) for lang in self.langues)  

        if total_chars > 4000:  
            body_class = "compress-plus"  
        elif total_chars > 2500:  
            body_class = "compress"  
        else:  
            body_class = "normal"  

        context = {  
            "infos": self.data,  
            "experiences": self.experiences,  
            "competences": self.competences,  
            "formations": self.formations,  
            "langues": self.langues,  
            "body_class": body_class  
        }  

        html = template.render(context)  

        nom = self.data.get('nom', 'cv').replace(" ", "_").lower()  
        nom_fichier = f"{nom}_moderne.pdf"  

        dossier = "generated_cv"  
        os.makedirs(dossier, exist_ok=True)  
        chemin_complet = os.path.join(dossier, nom_fichier)  

        HTML(string=html, base_url='Template/Moderne').write_pdf(chemin_complet)  

        return chemin_complet  

    def test_modern_cv_generator(self):  
        from jinja2 import Environment, FileSystemLoader  
        from weasyprint import HTML  
        import os  

        data = {  
            "infos": {  
                "nom": "DUPONT",  
                "prenom": "Jean",  
                "poste": "Développeur Python Senior",  
                "ville": "Paris, France",  
                "tel": "+33 6 12 34 56 78",  
                "email": "j.dupont@email.com",  
                "autre": "https://linkedin.com/in/jdupont",  
                "resume": "Développeur Python avec 5+ ans d'expérience dans le développement backend et l'analyse de données. Expert en Django, Flask et Pandas. Passionné par l'optimisation des performances et les architectures microservices."  
            },  
            "experiences": [  
                {  
                    "poste": "Développeur Backend Senior",  
                    "entreprise": "TechCorp",  
                    "date": "2020 - Présent",  
                    "description": "Conception d'APIs RESTful pour une plateforme SaaS avec Django.",  
                    "realisations": "Migration réussie vers Kubernetes, amélioration des temps de réponse de 40%."  
                },  
                {  
                    "poste": "Développeur Python",  
                    "entreprise": "DataSystems",  
                    "date": "2018 - 2020",  
                    "description": "Développement de scripts ETL pour le traitement de données clients.",  
                    "realisations": "Automatisation de rapports mensuels économisant 20h/mois."  
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

        nb_exp = len(data["experiences"])  
        nb_comp = len(data["competences"])  
        nb_form = len(data["formations"])  
        nb_lang = len(data["langues"])  
        taille_resume = len(data["infos"].get("resume", ""))  

        total_points = nb_exp * 2 + nb_comp + nb_form * 1.5 + nb_lang + (taille_resume // 100)  

        if total_points > 20:  
            compression = "compress-plus"  
        elif total_points > 14:  
            compression = "compress"  
        else:  
            compression = "normal"  

        context = {  
            "infos": data["infos"],  
            "experiences": data["experiences"],  
            "formations": data["formations"],  
            "competences": data["competences"],  
            "langues": data["langues"],  
            "compression": compression  
        }  

        env = Environment(loader=FileSystemLoader('Template/Moderne'))  
        template = env.get_template('Mod.html')  

        html_render = template.render(context)  

        nom = data["infos"]["nom"].lower().replace(" ", "_")  
        file_name = f"{nom}_moderne_test.pdf"  

        output_dir = "generated_cv"  
        os.makedirs(output_dir, exist_ok=True)  
        file_path = os.path.join(output_dir, file_name)  

        HTML(string=html_render, base_url='Template/Moderne').write_pdf(file_path)  

        print(f"✅ CV généré : {file_path} (compression: {compression})")  
        return file_path
