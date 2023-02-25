#Created by Mariia Verbytska
import datetime as dt
import json

import requests
from flask import Flask, jsonify, request

import datetime as dt
import json

import requests
from flask import Flask, jsonify, request
import csv
import codecs
import urllib.request
import urllib.error
import sys
from datetime import datetime, timezone

# create your API token, and set it up in Postman collection as part of the Body section
API_TOKEN = ""
API_KEY = ""

# include sections
# values include days,hours,current,alerts
include = "days"

app = Flask(__name__)


def gen_weather_from(location, start_date, end_date):
    base_url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/"

    сontent_type = "json"
    unit_group = "metric"
    include = "days"
    
    api_query = base_url + location

    # append the start date
    if (len(start_date)):
        api_query += "/" + start_date
    # append the end date (optional)
        if (len(end_date)):
            api_query += "/" + end_date

    
    api_query += "?"

    # append each parameter as necessary
    if (len(unit_group)):
        api_query += "&unitGroup=" + unit_group

    if (len(сontent_type)):
        api_query += "&contentType=" + сontent_type

    if (len(include)):
        api_query += "&include=" + include

    api_query += "&key=" + API_KEY
    CSVBytes = None
    try:
        CSVBytes = urllib.request.urlopen(api_query)
    except urllib.error.HTTPError as e:
        ErrorInfo = e.read().decode()
        print('Error code: ', e.code, ErrorInfo)
        sys.exit()
    except  urllib.error.URLError as e:
        ErrorInfo = e.read().decode()
        print('Error code: ', e.code, ErrorInfo)
        sys.exit()


    return CSVBytes


class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv["message"] = self.message
        return rv


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.route("/")
def home_page():
    return "<p><h2>Weather forecast test by Mariia Verbytska.</h2></p>"


@app.route(
    "/content/api/v1/integration/generate",
    methods=["POST"],
)

def endpoint():
    start_dt = datetime.now(timezone.utc)
    json_data = request.get_json()

    if json_data.get("token") is None:
        raise InvalidUsage("token is required", status_code=400)

    token = json_data.get("token")

    if token != API_TOKEN:
        raise InvalidUsage("wrong API token", status_code=403)

    requester_name = ""
    if json_data.get("requester_name"):
        requester_name = json_data.get("requester_name")
    location = ""
    if json_data.get("location"):
        location = json_data.get("location")
    start_date = ""
    if json_data.get("start_date"):
        start_date = json_data.get("start_date")
    end_date = ""
    if json_data.get("end_date"):
        end_date = json_data.get("end_date")

    
    weather = gen_weather_from(location, start_date, end_date)
    data = json.load(weather)
    if data.get("days"):
        info = data.get("days")
    else: 
        info = "Empty"
    result = {
        "requester_name": requester_name,
        
        "timestamp": start_dt,
        
        "location": location,
        
        "days": start_date+":"+end_date,
        
         "weather": info

    }

    return result
