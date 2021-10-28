import json
import os
import sys
import django
from constants import *

### Need to setup django before importing django models ###
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
sys.path.append(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "web.settings")
django.setup()
####### 

from googleapiclient.discovery import build
from helper import empty_table_in_spreadsheet

def autofill_category(sheet, category_model, category_range):
    data = []
    pk_counter = 999999
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=category_range).execute()
    categories = result.get('values', [])

    if not categories:
        raise Exception(empty_table_in_spreadsheet(SPREADSHEET_ID, range=category_range))
    
    for row in categories[1:]:
        category = {
            "model": f"{category_model}",
            "pk": pk_counter,
            "fields": {
                "name": row[categories[0].index("name")],
                "description": row[categories[0].index("description")]
            }
        }
        pk_counter +=1
        data.append(category)

    return data

def main():
    # Building the service used to call the Sheet API
    service = build('sheets', 'v4', developerKey=API_KEY)
    spreadsheet = service.spreadsheets()

    data = []
    requirements_data = autofill_category(spreadsheet, "happenings.requirementcategory", req_range)
    interests_data = autofill_category(spreadsheet, "happenings.interestcategory", interest_range)
    
    data.extend(requirements_data)
    data.extend(interests_data)

    with open(f"{PATH}/{CATEGORIES_FILE}", "w") as output:
        json.dump(data, output, indent=4)
        output.write("\n")

if __name__ == '__main__':
    main()
