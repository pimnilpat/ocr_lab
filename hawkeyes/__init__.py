import os
from flask import Flask
from .api import hawkeyes

from datetime import timedelta

def create_hawkeye(config=None):
    
    #__name__ is the name of current module
    #instance_relative_config=True for tell app that configuration files are relative to instance folder, it can hold local data that shouldn’t be committed to version control, such as configuration secrets and the database file.
    
    app = Flask(__name__,  instance_relative_config=True) 

    #Or we can specific the static folder as below
    #app = Flask(__name__, static_folder="/path/folder_static")

    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])  #Allow extensions for file uploads
    
    #set some default configuration    
    app.config.from_mapping(
        ENV = "development",
        DEBUG = True,
        PERMANENT_SESSION_LIFETIME = timedelta(minutes=15),
        SECRET_KEY = "development",  #SECRET_KEY is used by Flask and extensions to keep data safe
        DATABASE = os.path.join(app.instance_path, "api.sqlite"),   #DATABASE is the path where the SQLite database file will be saved
        UPLOAD_FOLDER = os.path.join(app.instance_path, "uploads"), #Upload folder
        MAX_CONTENT_LENGTH = 16 * 1024 * 1024,   #Define maximum file size upload   
        ALLOWED_EXTENSIONS = ALLOWED_EXTENSIONS,
        JSONIFY_PRETTYPRINT_REGULAR = True
    )
    
    if config is None:
        #Load the instance config,  if it exits,
        #Overides the default configuration with values taken from the config.py file in the intance folder if it exits.
        app.config.from_pyfile("config.py", silent=True) #silent = True is if not found config.py in instance folder then will suppress error message
    else:
        app.config.from_mapping(config)

    
    try:
        os.makedirs(app.instance_path) #Create folder of instance path, default name  = instance
    except OSError:
        pass

    try:
        os.makedirs(os.path.join(app.instance_path, "uploads"), exist_ok=True)   #Create upload folder directory inside instance path

    except OSError:
        pass

    '''
    Call API
    '''
    hawkeyes(app)


    return app