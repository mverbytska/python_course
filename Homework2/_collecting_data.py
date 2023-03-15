#!/usr/bin/env python
# coding: utf-8




import requests 
from bs4 import BeautifulSoup
import os 
from datetime import date, timedelta




# start and end date of diapasone
START = date(2022, 2, 25)
END = date(2023, 1, 20)

# create a directory if it does not exist
if not os.path.exists('/Users/mashaverbytskaya/python_course/my_env/isw_data'): #Paste your directory here
    os.makedirs('/Users/mashaverbytskaya/python_course/my_env/isw_data')

# Go through all the dates in the diapasone(25 febr 2022 - 20 jan 2023)
CURRENTday = START
while CURRENTday <= END:
    # URL for requests, they can be different depending on date and year
    if CURRENTday.year == 2022:
        if CURRENTday.month == 2 and CURRENTday.day == 25:
            url = f'https://www.understandingwar.org/backgrounder/russia-ukraine-warning-update-russian-offensive-campaign-assessment-february-25-2022'
        elif CURRENTday.month == 2 and (CURRENTday.day == 26 or CURRENTday.day == 27):
            url = f'https://www.understandingwar.org/backgrounder/russia-ukraine-warning-update-russian-offensive-campaign-assessment-{CURRENTday.strftime("%B")}-{CURRENTday.strftime("%d").lstrip("0")}'
        elif CURRENTday.month == 2 and CURRENTday.day == 28:
            url = f'https://www.understandingwar.org/backgrounder/russian-offensive-campaign-assessment-february-28-2022'
        elif CURRENTday.month == 3 and CURRENTday.day == 3:
            url = f'https://www.understandingwar.org/backgrounder/ukraine-conflict-update-14'
        elif CURRENTday.month == 3 and CURRENTday.day == 4:
            url = f'https://www.understandingwar.org/backgrounder/ukraine-conflict-update-15'
        elif CURRENTday.month == 3 and CURRENTday.day == 6:
            url = f'https://www.understandingwar.org/backgrounder/ukraine-conflict-update-16'
        elif CURRENTday.month == 3 and CURRENTday.day == 5:
            url = f'https://www.understandingwar.org/backgrounder/explainer-russian-conscription-reserve-and-mobilization'
        else:
            url = f'https://www.understandingwar.org/backgrounder/russian-offensive-campaign-assessment-{CURRENTday.strftime("%B")}-{CURRENTday.strftime("%d").lstrip("0")}'
    elif CURRENTday.year == 2023:
        url = f'https://www.understandingwar.org/backgrounder/russian-offensive-campaign-assessment-{CURRENTday.strftime("%B")}-{CURRENTday.strftime("%d").lstrip("0")}-{CURRENTday.year}'


    # Make a request
    response = requests.get(url)

    # Save html file into the directory if the request was successful.
    if response.status_code == 200:
        file_path = f'/Users/mashaverbytskaya/python_course/my_env/isw_data/{CURRENTday}.html' #Paste your directory here
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(response.text)

    # iterate to next dat using timedelta from lib
    CURRENTday += timedelta(days=1)







