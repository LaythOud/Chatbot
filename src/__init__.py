from flask import Flask
from src.database import db
from src.services import cv_analyse
from src.config import SECRET_KEY, DATABASE_PATH, root_directory
import os
from flask_limiter import Limiter, util

def _init_db(app):
    """Initialize the database with the Flask app."""
    db.init_app(app)
    with app.app_context():
        db.create_all()
        cv_analyse.CVAnalyse.analyse()

def _initialize_blueprints(application):
    '''
    Register Flask blueprints
    '''
    from src.views.chatbot import chatbot
    
    application.register_blueprint(chatbot, url_prefix='/chatbot/')
    

def create_app():
    '''
    Create an app by initializing components.
    '''
    open(root_directory + "/app.log", "w").close()
    application = Flask(__name__, template_folder=root_directory + '/templates')
    application.secret_key = SECRET_KEY
    os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
    
    application.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DATABASE_PATH}'
    application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    Limiter(
        util.get_remote_address,
        app=application,
        default_limits=["50 per day"],
        storage_uri="memory://",
    )
    _init_db(application)
    _initialize_blueprints(application)

    return application

