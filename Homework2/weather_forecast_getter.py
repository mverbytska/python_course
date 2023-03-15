


import json
import requests
import sys
import re
import pandas as pd
from datetime import datetime, timedelta 

API_KEY = ''
BASE_URL = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline'
unit_group = 'metric'




# Returns the weather forecast for the following 12 hours
def get_12hr_forecast(location: str) -> list:
    
    date_start = datetime.now().replace(minute=0, second=0)
    date_end = date_start + timedelta(hours=12)
    dt_format = '%Y-%m-%dT%H:%M:%S'
    date_start, date_end = date_start.strftime(dt_format), date_end.strftime(dt_format) 
    
    api_query = f'{BASE_URL}/{location}/{date_start}/{date_end}?unitGroup={unit_group}&key={API_KEY}&contentType=json'

    response = requests.request("GET", url=api_query)
    if response.status_code != 200:
        print('Unexpected Status code: ', response.status_code)
        sys.exit() 
    
    data = strip_irrelevant_data(response.json(), date_start, date_end)
    
    return data


# Deletes the json entries outside of the relevant 12-hour forecast timeframe
def strip_irrelevant_data(data: dict, date_start: str, date_end: str) -> list:
    
    data_1 = data['days'][0]['hours']
    data_1 = data_1[datetime.strptime(date_start, '%Y-%m-%dT%H:%M:%S').time().hour:]
    
    if len(data) > 1:
        data_2 = data['days'][1]['hours']
        data_2 = data_2[:datetime.strptime(date_end, '%Y-%m-%dT%H:%M:%S').time().hour]
        return data_1 + data_2
    
    return data_1




data = get_12hr_forecast('Kyiv, Ukraine')
data


df = pd.DataFrame(data)
df = df.set_index('datetime')
df

