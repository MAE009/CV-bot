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

    def test_modern_cv_generator(self, cv_type, template_file):
    """
    Génère un CV moderne avec adaptation automatique de la mise en page
    selon la quantité de contenu.
    
    Args:
        cv_type (str): Type de template ('moderne', 'classique', etc.)
        template_file (str): Nom du fichier template sans extension
        
    Returns:
        str: Chemin du fichier PDF généré
    """
    try:
        # Chargement des données de test
        data = test_data
        
        # Configuration de l'environnement Jinja2
        template_dir = f'Template/{cv_type}'
        env = Environment(
            loader=FileSystemLoader(template_dir),
            autoescape=select_autoescape(['html', 'xml'])
        )
        template = env.get_template(f'{template_file}.html')

        # Calcul du score de densité de contenu
        content_metrics = {
            'experiences': len(data["experiences"]),
            'competences': len(data["competences"]),
            'formations': len(data["formations"]),
            'langues': len(data["langues"]),
            'resume_length': len(data["infos"].get("resume", ""))
        }
        
        # Pondération différente pour chaque section
        content_score = (
            content_metrics['experiences'] * 2 + 
            content_metrics['competences'] * 1 +
            content_metrics['formations'] * 1.5 +
            content_metrics['langues'] * 1 +
            (content_metrics['resume_length'] // 100)
        )

        # Sélection du mode de compression adaptatif
        if content_score > 20:
            body_class = "compress-plus"
        elif content_score > 14:
            body_class = "compress"
        else:
            body_class = "normal"

        # Préparation du contexte
        context = {
            "body_class": body_class,
            "infos": data["infos"],
            "experiences": data["experiences"],
            "formations": data["formations"],
            "competences": data["competences"],
            "langues": data["langues"],
            "content_score": content_score,  # Pour debug éventuel
            "generation_date": datetime.now().strftime("%Y-%m-%d")
        }

        # Rendu du template
        html_content = template.render(context)

        # Génération du nom de fichier
        safe_name = data["infos"]["nom"].lower().replace(" ", "_")
        output_filename = f"{safe_name}_{cv_type}_{body_class}.pdf"
        
        # Création du répertoire de sortie
        output_dir = "generated_cv"
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, output_filename)

        # Conversion en PDF avec des paramètres optimisés
        HTML(
            string=html_content,
            base_url=template_dir
        ).write_pdf(
            output_path,
            stylesheets=[CSS(string='@page { size: A4; margin: 1cm; }')],
            optimize_size=('fonts', 'images', 'content')
        )

        # Log de confirmation
        print(f"CV généré avec succès: {output_path} | Mode: {body_class} | Score: {content_score}")
        return output_path

    except Exception as e:
        print(f"Erreur lors de la génération du CV: {str(e)}")
        raise
