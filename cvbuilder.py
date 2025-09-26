from telegram import InputFile  
from jinja2 import Environment, FileSystemLoader, select_autoescape  
from weasyprint import HTML, CSS  
import os  
from datetime import datetime  
from bank_text import *
from Tools.capture_image import *
import base64


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
        self.photo_path = ""
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
        env = Environment(loader=FileSystemLoader('Template/ATS'))  
        template = env.get_template('ats.html')  

        nb_exp = len(self.experiences)  
        nb_comp = len(self.competences)  
        nb_form = len(self.formations)  
        nb_lang = len(self.langues)  
        taille_resume = len(self.data["resume"])  

        total_points = nb_exp * 2 + nb_comp + nb_form * 1.5 + nb_lang + (taille_resume // 100)  

        if total_points > 20:  
            body_class = "compress-plus"  
        elif total_points > 14:  
            body_class = "compress"  
        else:  
            body_class = "normal"  
        
        context = {  
            "infos": self.data,  
            "experiences": self.experiences,  
            "competences": self.competences,  
            "formations": self.formations,  
            "langues": self.langues,  
            "body_class": body_class,
            "photo_path" : self.photo_path
        }  

        html = template.render(context)  

        nom = self.data.get('nom', 'cv').replace(" ", "_").lower()  
        nom_fichier = f"{nom}_ats.pdf"  

        dossier = "generated_cv"  
        os.makedirs(dossier, exist_ok=True)  
        chemin_complet = os.path.join(dossier, nom_fichier)  

        HTML(string=html, base_url='Template/ATS').write_pdf(chemin_complet)  

        return chemin_complet  

    def creative_cv(self):  
        env = Environment(loader=FileSystemLoader('Template/Creative'))  
        template = env.get_template('Crea.html')

        with open(self.photo_path, "rb") as f:
            img_data = f.read()
        photo_b64 = "data:image/jpeg;base64," + base64.b64encode(img_data).decode()


        nb_exp = len(self.experiences)  
        nb_comp = len(self.competences)  
        nb_form = len(self.formations)  
        nb_lang = len(self.langues)  
        taille_resume = len(self.data["resume"])  

        total_points = nb_exp * 2 + nb_comp + nb_form * 1.5 + nb_lang + (taille_resume // 100)  

        if total_points > 20:  
            body_class = "compress-plus"  
        elif total_points > 14:  
            body_class = "compress"  
        else:  
            body_class = "normal"  

        context = {  
            "infos": self.data,  
            "experiences": self.experiences,  
            "competences": self.competences,  
            "formations": self.formations,  
            "langues": self.langues,  
            "body_class": body_class,
            "photo_path" : photo_b64
        }  

        html_render = template.render(context)  

        nom = self.data["nom"].lower().replace(" ", "sans_nom")  
        file_name = f"{nom}_CV_creative.pdf"  

        output_dir = "generated_cv"  
        os.makedirs(output_dir, exist_ok=True)  
        file_path = os.path.join(output_dir, file_name)  

        HTML(string=html_render, base_url='Template/Creative').write_pdf(file_path)  

        return file_path  

    def moderne_cv(self):  
        env = Environment(loader=FileSystemLoader('Template/Moderne'))  
        template = env.get_template('Mod.html')
        

        with open(self.photo_path, "rb") as f:
            img_data = f.read()
        photo_b64 = "data:image/jpeg;base64," + base64.b64encode(img_data).decode()



        nb_exp = len(self.experiences)  
        nb_comp = len(self.competences)  
        nb_form = len(self.formations)  
        nb_lang = len(self.langues)  
        taille_resume = len(self.data["resume"])  

        
        total_points = nb_exp * 2 + nb_comp + nb_form * 1.5 + nb_lang + (taille_resume // 100)  

        if total_points > 20:  
            body_class = "compress-plus"  
        elif total_points > 14:  
            body_class = "compress"  
        else:  
            body_class = "normal"  

        context = {  
            "infos": self.data,  
            "experiences": self.experiences,  
            "competences": self.competences,  
            "formations": self.formations,  
            "langues": self.langues,  
            "body_class": body_class,
            "photo_path" : photo_b64
        }  

        html = template.render(context)  

        nom = self.data.get('nom', 'cv').replace(" ", "_").lower()  
        nom_fichier = f"{nom}_CV_moderne.pdf"  

        dossier = "generated_cv"  
        os.makedirs(dossier, exist_ok=True)  
        chemin_complet = os.path.join(dossier, nom_fichier)  

        HTML(string=html, base_url='Template/Moderne').write_pdf(chemin_complet)  

        return chemin_complet  

    

    def test_modern_cv_generator(self, cv_type, template_file):
        """
        Génère un CV moderne et son image LinkedIn
        """
        data = test_data_duc
        try:
            # 1️⃣ Préparation de la photo
            with open(data['photo_path'], "rb") as f:
                img_data = f.read()
            photo_b64 = "data:image/jpeg;base64," + base64.b64encode(img_data).decode()

            env = Environment(loader=FileSystemLoader(f'Template/{cv_type}'))  
        
            template = env.get_template(f'{template_file}.html')

            # 3️⃣ Calcul du content_score
            content_metrics = {
                'experiences': len(data["experiences"]),
                'competences': len(data["competences"]),
                'formations': len(data["formations"]),
                'langues': len(data["langues"]),
                'resume_length': len(data["infos"].get("resume", ""))
            }

            content_score = (
                content_metrics['experiences'] * 3 +
                content_metrics['competences'] * 1 +
                content_metrics['formations'] * 2 +
                content_metrics['langues'] * 0.5 +
                min(content_metrics['resume_length'] // 80, 10)
            )

            # 4️⃣ Détermination du niveau de compression
            if content_score > 25:
                body_class = "compress-plus"
                compression_level = "ultra"
            elif content_score > 18:
                body_class = "compress"
                compression_level = "medium"
            elif content_score > 12:
                body_class = "compact"
                compression_level = "light"
            else:
                body_class = "normal"
                compression_level = "none"

            # 5️⃣ Préparation du contexte pour le template
            context = {
                "body_class": body_class,
                "infos": data["infos"],
                "experiences": data["experiences"],
                "formations": data["formations"],
                "competences": data["competences"],
                "langues": data["langues"],
                "photo_path": photo_b64,
                "content_score": content_score,
                "generation_date": datetime.now().strftime("%Y-%m-%d")
            }

            # 6️⃣ Génération du HTML
            html = template.render(context)  

            nom = data['infos']['nom'].replace(" ", "_").lower()  
            nom_fichier = f"{data['infos']['nom']}_CV_{cv_type}.pdf"  

            dossier = "generated_cv"  
            os.makedirs(dossier, exist_ok=True)  
            chemin_complet = os.path.join(dossier, nom_fichier)  

            HTML(string=html, base_url=f'Template/{cv_type}').write_pdf(chemin_complet)  

            return chemin_complet  
            

        except Exception as e:
            print(f"❌ Erreur CV generation: {str(e)}")
            raise
