# Importing required libraries
from flask import Flask
import os
from api.model.required_functions import readYAML
from api.model.views import api, load_data
import logging
import logging.config
import warnings

warnings.filterwarnings('ignore')

app = Flask(__name__)

# Current App Folder Name
folder_name = "api"

# Getting the current working directory
current_working_dir = os.getcwd()

def create_app():
    # Setting the app config
    data = readYAML(os.path.join(current_working_dir, folder_name, "config", "config.yaml"))
    # Updating the app config with the data from the config.yaml file
    app.config.update(data["DEVELOPMENT"])

    past_data_file_location = os.path.join(current_working_dir, folder_name, app.config["data_folder"], app.config["past_data_file_location"])

    # Reading the past data pickle file
    load_data(past_data_file_location, "past_data")

    xgb_model_file_location = os.path.join(current_working_dir, folder_name, app.config["data_folder"], app.config["xgb_model_file_location"])

    # Reading the xgb model pickle file
    load_data(xgb_model_file_location, "")

    # Setting basic config for logs
    logging.basicConfig(
        level=logging.DEBUG,
        format=app.config["LOG_FORMAT"]
    )

    logger = logging.getLogger(__name__)
    formatter = logging.Formatter(app.config["LOG_FORMAT"])
    with app.app_context():        
        # Register api Blueprint
        app.register_blueprint(api)
        return app