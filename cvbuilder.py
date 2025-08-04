from telegram import InputFile  
from jinja2 import Environment, FileSystemLoader  
from weasyprint import HTML  
import os  
from bank_text import *


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
            "body_class": body_class
        }  

        html = template.render(context)  

        nom = self.data.get('nom', 'cv').replace(" ", "_").lower()  
        nom_fichier = f"{nom}_ats.pdf"  

        dossier = "generated_cv"  
        os.makedirs(dossier, exist_ok=True)  
        chemin_complet = os.path.join(dossier, nom_fichier)  

        HTML(string=html, base_url='Template/ATS').write_pdf(chemin_complet)  

        return chemin_complet  

    
    
    def creative(self):  
        
        env = Environment(loader=FileSystemLoader('Template/Creative'))  
        template = env.get_template('Crea.html')

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
            "body_class": body_class
            
        }  

        html_render = template.render(context)  

        #nom = self.data.get('nom', 'cv').replace(" ", "_").lower() 
        nom = self.data["nom"].lower().replace(" ", "sans_nom")  
        file_name = f"{nom}_CV_creative.pdf"  

        output_dir = "generated_cv"  
        os.makedirs(output_dir, exist_ok=True)  
        file_path = os.path.join(output_dir, file_name)  

        HTML(string=html_render, base_url='Template/Creative').write_pdf(file_path)  

        #print(f"✅ CV généré : {file_path} (compression: {compress})")  
        return file_path
        
    def moderne_cv(self):  

        env = Environment(loader=FileSystemLoader('Template/Moderne'))  
        template = env.get_template('Mod.html')  

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
            "body_class": body_class  
        }  

        html = template.render(context)  

        nom = self.data.get('nom', 'cv').replace(" ", "_").lower()  
        nom_fichier = f"{nom}_CV_moderne.pdf"  

        dossier = "generated_cv"  
        os.makedirs(dossier, exist_ok=True)  
        chemin_complet = os.path.join(dossier, nom_fichier)  

        HTML(string=html, base_url='Template/Moderne').write_pdf(chemin_complet)  

        return chemin_complet  

    def test_modern_cv_generator(self, type, fichier):  
        
        data = test_data

        env = Environment(loader=FileSystemLoader(f'Template/{type}'))  
        template = env.get_template(f'{fichier}.html')


        nb_exp = len(data["experiences"])  
        nb_comp = len(data["competences"])  
        nb_form = len(data["formations"])  
        nb_lang = len(data["langues"])  
        taille_resume = len(data["infos"].get("resume", ""))  

        total_points = nb_exp * 2 + nb_comp + nb_form * 1.5 + nb_lang + (taille_resume // 100)  

        if total_points > 20:  
            body_class = "compress-plus"  
        elif total_points > 14:  
            body_class = "compress"  
        else:  
            body_class = "normal"  

        context = {
            "body_class": body_class,
            "infos": data["infos"],  
            "experiences": data["experiences"],  
            "formations": data["formations"],  
            "competences": data["competences"],  
            "langues": data["langues"],  
            "compress": body_class,
            "taill": total_points,
            
        }  

        html_render = template.render(context)  

        nom = data["infos"]["nom"].lower().replace(" ", "_")  
        file_name = f"{nom}_{type}_test.pdf"  

        output_dir = "generated_cv"  
        os.makedirs(output_dir, exist_ok=True)  
        file_path = os.path.join(output_dir, file_name)  

        HTML(string=html_render, base_url=f'Template/{type}').write_pdf(file_path)  

        #print(f"✅ CV généré : {file_path} (compression: {compress})")  
        return file_path
