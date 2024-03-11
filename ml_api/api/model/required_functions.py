# Importing required functions
import time
import datetime
import yaml
from flask import current_app
import traceback
import warnings

warnings.filterwarnings('ignore')

def readYAML(file: str):
    """
    Reads a YAML file and returns the parsed configuration.

    Args:
        file (str): The path to the YAML file.

    Returns:
        dict: The parsed configuration from the YAML file.
    """
    stream = open(file, "r")
    try:
        config = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        current_app.logger.critical(exc)
        current_app.logger.critical(traceback.format_exc(exc))
    stream.close()
    return config

def convert_to_unix(s):
    """
    Converts a string representation of a date and time to a Unix timestamp.

    Args:
        s (str): The string representation of the date and time in the format "%Y-%m-%d %H:%M:%S".

    Returns:
        float: The Unix timestamp corresponding to the input string.

    """
    s = str(s)
    return time.mktime(datetime.datetime.strptime(s, "%Y-%m-%d %H:%M:%S").timetuple())

def add_pickup_bins(timestamp):
    """
    Adds pickup bins to the given DataFrame

    Args:
        frame (DataFrame): The DataFrame to which pickup bins will be added.

    Returns:
        DataFrame: The updated DataFrame with pickup bins added.
    """
    
    start_pickup_unix = 1672511400
    tenminutewise_binned_unix_pickup_times = (int((timestamp - start_pickup_unix) / 600))
    bin_number = tenminutewise_binned_unix_pickup_times

    return bin_number

def predict_pickups(input_df, past_data, xgb_model):
    """
    This function predicts the pickup value for input location id at a particular time
    """
    # Converting Time stamps to UNIX time stamp format
    # "YYYY-MM-DD HH:MM:SS" into unix time stamp

    #Refer:https://www.unixtimestamp.com/
    # 1672511400 : 2023-01-01 00:00:00 
    # 1675189800 : 2023-02-01 00:00:00 
    # 1677609000 : 2023-03-01 00:00:00    
    
    # converting to unix time stamp
    input_df['PU_timestamp'] = input_df['PU_timestamp'].apply(convert_to_unix)
    # adding pickup bin number 
    input_df['bin_number'] = input_df['PU_timestamp'].apply(add_pickup_bins) 
    # Calculating the row number for the given bin number
    input_df['row_number'] = input_df['bin_number']  + (input_df['locationID'] * 12960)
    # Calculating the row number for the given bin number
    input_df['row_number'] = input_df['row_number'] - 5*(input_df['locationID']+1)
    
    # getting the feature row for the given bin number
    feature_row = past_data.iloc[input_df['row_number']]
    # reseting the index
    feature_row = feature_row.reset_index(drop=True)
    # print(feature_row)
    
    # predicting the number of pickups
    y_pred = xgb_model.predict(feature_row)
    output = round(y_pred[0])
    
    return output