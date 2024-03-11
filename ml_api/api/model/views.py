from flask import Blueprint, current_app, request, jsonify
from api.model.required_functions import predict_pickups
import traceback
import warnings
import pandas as pd
import pickle

warnings.filterwarnings('ignore')

api = Blueprint('api', __name__)

past_data = pd.DataFrame()
xgb_model = ""

def load_data(file_location, file_type):
    """
    Load data from a pickle file.

    Args:
        file_location (str): The location of the pickle file.
        file_type (str): The type of data to load. Can be either "past_data" or "xgb_model".

    Returns:
        dict: If an error occurs during loading, a dictionary with an error message is returned.
    """
    try:
        global past_data
        global xgb_model
        if file_type == "past_data":
            # Reading the past data pickle file
            past_data = pickle.load(open(file_location, 'rb'))
        else:
            # Reading the xgb model pickle file
            xgb_model = pickle.load(open(file_location, 'rb'))
    except Exception as e:
        errorMsg = {'message':e}
        current_app.logger.error(errorMsg)
        current_app.logger.error(traceback.format_exc())
        return errorMsg

# API endpoint1
@api.route('/predict_pickups/',methods=['POST', 'GET'])
def first_endpoint():
    try:
        if request.method == 'POST':
            request_data = request.get_json()
            try:
                # Fetch names locationID and timestamp from Body
                input_locationID = request_data["locationID"]
                input_timestamp = request_data["PU_timestamp"]
                data = {'locationID': [input_locationID],
                        'PU_timestamp': [input_timestamp]}
                input_df = pd.DataFrame(data)
                
                # Pass the input request df, past_data and model
                # to the predict_pickup function
                predicted_val = predict_pickups(input_df, past_data, xgb_model)
                # Initialize output dictionary
                output_json = {}
                output_json["predicted_pickups"] = predicted_val
                current_app.logger.info(str(output_json))
                return output_json
            except Exception as e:
                # Handling error
                errorMsg = {'message':'error in predicting the value'}
                current_app.logger.error(errorMsg)
                current_app.logger.error(traceback.format_exc())
                return errorMsg 
        elif request.method == 'GET':
            return jsonify({
                "status": 200,
                "description": "The application is working."
            })
        else:
            return jsonify({
                "status" : 442,
                "description" : "Invalid Method Type"
            })
    except Exception as e:
        # Handling error
        errorMsg = {'message':'error in predicting the value'}
        current_app.logger.error(errorMsg)
        current_app.logger.error(traceback.format_exc())
        return errorMsg