from .cv_handlers import setup_cv_handlers
from .menu_handlers import setup_menu_handlers
from .models_handlers import setup_models_handlers
from utils.helpers import setup_helpers



async def setup_handlers(app):
    setup_menu_handlers(app)
    setup_cv_handlers(app)
    setup_models_handlers(app)
    setup_helpers(app)
