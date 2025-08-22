from telegram import InputFile  
from jinja2 import Environment, FileSystemLoader, select_autoescape  
from weasyprint import HTML, CSS  
import os  
from datetime import datetime  
from bank_text import *
from Tools.capture_image import *


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
        nom_fichier = f"{nom}_CV_moderne.pdf"  

        dossier = "generated_cv"  
        os.makedirs(dossier, exist_ok=True)  
        chemin_complet = os.path.join(dossier, nom_fichier)  

        HTML(string=html, base_url='Template/Moderne').write_pdf(chemin_complet)  

        return chemin_complet  

    def  test_modern_cv_generator(self, cv_type, template_file):  
        """Génère un CV moderne et son image LinkedIn"""  
        try:  
            data = test_data  
            template_dir = f'Template/{cv_type}'
            
            # 1. Préparation du template
            env = Environment(
                loader=FileSystemLoader(template_dir),
                autoescape=select_autoescape(['html', 'xml'])
            )
            template = env.get_template(f'{template_file}.html')

            # ... (votre logique existante de calcul du content_score) ...
            content_metrics = {  
                'experiences': len(data["experiences"]),  
                'competences': len(data["competences"]),  
                'formations': len(data["formations"]),  
                'langues': len(data["langues"]),  
                'resume_length': len(data["infos"].get("resume", ""))  
            }  

            content_score = (  
                content_metrics['experiences'] * 2 +  
                content_metrics['competences'] * 1 +  
                content_metrics['formations'] * 1.5 +  
                content_metrics['langues'] * 1 +  
                (content_metrics['resume_length'] // 100)  
            )  

            if content_score > 20:  
                body_class = "compress-plus"  
            elif content_score > 14:  
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
                "content_score": content_score,  
                "generation_date": datetime.now().strftime("%Y-%m-%d")  
            }  
            # 2. Génération du HTML
            html_content = template.render(context)
            safe_name = data["infos"]["nom"].lower().replace(" ", "_")
            output_dir = "generated_cv"
            os.makedirs(output_dir, exist_ok=True)

            # 3. Sauvegarde du HTML temporaire
            html_temp_path = os.path.join(output_dir, f"temp_{safe_name}.html")
            with open(html_temp_path, "w", encoding="utf-8") as f:
                f.write(html_content)

            # 4. Génération PDF
            pdf_path = os.path.join(output_dir, f"{safe_name}_{cv_type}.pdf")
            HTML(string=html_content, base_url=template_dir).write_pdf(
                pdf_path,
                stylesheets=[CSS(string='@page { size: A4; margin: 1cm; }')]
            )

            # 5. Génération image LinkedIn
            css_path = os.path.join(template_dir, f"{template_file}.css")
            linkedin_image_path = html_to_linkedin_image(
                html_path=html_temp_path,
                css_path=css_path
            )

            # Nettoyage du HTML temporaire
            os.remove(html_temp_path)

            return pdf_path, linkedin_image_path

        except Exception as e:  
            print(f"❌ Erreur CV generation: {str(e)}")  
            raise
