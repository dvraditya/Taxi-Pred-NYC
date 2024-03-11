
# NYC Yellow Taxi Prediction

## Problem Statement
Given location ID and time as input, the goal is to build a model which can predict the number of pickups by an yellow taxi in the query region and surrounding regions.

## Data Description

Dataset consists of 3 types of taxi data. Yellow Taxi, FHVs (For Hire Vehicles) and Green Taxi: Street Hail Livery (SHL). For this task I am only considering yellow taxi data between Jan - Mar 2022 & Jan - Mar 2023.

Data Download Link:

https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page

Data Dictionary Link: 

https://www.nyc.gov/assets/tlc/downloads/pdf/data_dictionary_trip_records_yellow.pdf

NYC yellow taxi trip data consists of detailed records on individual taxi rides. This data, provided by the NYC Taxi and Limousine Commission (TLC), includes information like pick-up and drop-off locations and times, trip distance, passenger count, fare details, and even payment methods.




## How to Run

Install all dependencies in your environment using requirements.txt

```bash
  pip install -r requirements.txt
```
1) Perform a basic EDA of the dataset by running EDA.py
2) Perform data cleaning by running Data_Processing.ipynb
3) Perform Data transformation and model training by running Data Transform.py
4) To Test the model, run main file.ipynb along with desired input parameters

## Deployment

To deploy this project on Docker, run

```bash
  docker run -d -p 8081:8081 moto_api
```
Post deployment, send a POST request to localhost at 8081 port with input parameters

You can access the API at the following endpoint: `http://127.0.0.1:8081/predict_pickups/`


### Sample Input JSON:

#### Get all items

```http
  POST /predict_pickups/
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `locationID` | `integer` | **Required**. Pickup locationID |
| `PU_timestamp` | `string` | **Required**. Pickup timestamp |

