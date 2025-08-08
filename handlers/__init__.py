from .cv_handlers import setup_cv_handlers
from .menu_handlers import setup_menu_handlers
from .models_handlers import setup_models_handlers

def setup_handlers(app):
    setup_menu_handlers(app)
    setup_cv_handlers(app)
    setup_models_handlers(app)
