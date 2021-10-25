import json
import os
import sys
import django

### Need to setup django before importing django models ###
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
sys.path.append(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "web.settings")
django.setup()
####### 

from dotenv import load_dotenv
from googleapiclient.discovery import build
from django.utils import timezone
from django.conf import settings
from happenings.models import InterestCategory, RequirementCategory


def empty_table_in_spreadsheet(sheet_id, sheet_range):
    return f"Spreadsheet {sheet_id} does not contain data at range {sheet_range}"

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

def get_categories_list_with_pk(categories, category_type):
    categories = list(map(str.strip, categories.split(',')))
    
    # Can be rewritten to use match-case in python 3.10
    if category_type.lower() == "interest":
        for index, name in enumerate(categories):
            categories[index] = InterestCategory.objects.get(name=name).id
        return categories

    elif category_type.lower() == "requirement":
        for index, name in enumerate(categories):
            categories[index] = RequirementCategory.objects.get(name=name).id
        return categories


def autofill_events(sheet):
    data = []
    pk_counter = 99999

    # Building the service used to call the Sheet API
    service = build('sheets', 'v4', developerKey=API_KEY)
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=event_range).execute()
    events = result.get('values', [])

    if not events:
        raise Exception(empty_table_in_spreadsheet(SPREADSHEET_ID, event_range))

    for row in events[1:]:
        event_pk = pk_counter+1
        event = {
                "model": "happenings.event",
                "pk": event_pk,
                "fields": {
                    "name": row[events[0].index("name")],
                    "location": row[events[0].index("location")],
                    "min_price": row[events[0].index("min_price")],
                    "max_price": row[events[0].index("max_price")],
                    "short_description": row[events[0].index("short_description")],
                    "description": row[events[0].index("description")],
                    "image": row[events[0].index("image")],
                    "admin_approved": bool(row[events[0].index("admin_approved")]),
                    "interest_categories": get_categories_list_with_pk(row[events[0].index("interest_categories")], "interest"),
                    "requirement_categories": get_categories_list_with_pk(row[events[0].index("requirement_categories")], "requirement"),
                    "host": "1",
            }
        }

        data.append(event)
        pk_counter +=1
        
        # Set the event to 30 days from now with a duration of 4 hours
        start_time = timezone.now() + timezone.timedelta(days=30)
        end_time = timezone.now() + timezone.timedelta(days=30, hours=4)
        schedule = {
            "model": "happenings.schedule",
            "pk": pk_counter,
            "fields": {
                "start_time": start_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
                "end_time": end_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
                "event": event_pk
            }
        }

        data.append(schedule)
    
    return data


def main():
    # Building the service used to call the Sheet API
    service = build('sheets', 'v4', developerKey=API_KEY)
    spreadsheet = service.spreadsheets()
    
    data = []
    requirements_data = autofill_category(spreadsheet, "happenings.requirementcategory", req_range)
    interests_data = autofill_category(spreadsheet, "happenings.interestcategory", interest_range)
    events_data = autofill_events(spreadsheet)
    
    data.extend(requirements_data)
    data.extend(interests_data)
    data.extend(events_data)

    with open(f"{path}/{filename}", "w") as output:
        json.dump(data, output, indent=4)
        output.write("\n")


if __name__ == '__main__':
    # Configuration: Environment variables

    dotenv_file = os.path.join(BASE_DIR, ".env")
    
    if os.path.isfile(dotenv_file):
        load_dotenv(dotenv_file)
    
    API_KEY = os.environ['SHEET_KEY']

    path = "happenings/fixtures"
    filename = "events.json"

    #### Spreadsheet values in the "Auto fill" data sheet ####
    SPREADSHEET_ID = "1R7xoCYJUm_pgVj7j80cZBEhBUprw1mPLx069Zz9uYfY"

    # Events
    event_sheet = "Events"
    event_start = "A1"  
    event_end = "K19"
    event_range = f"{event_sheet}!{event_start}:{event_end}"

    ### Categories ###
    categories_sheet = "Categories"

    # Requirements categories
    req_start = "A2"
    req_end = "B14"
    req_range = f"{categories_sheet}!{req_start}:{req_end}"

    # Interest categories
    interest_start = "E2"
    interest_end = "F19"
    interest_range = f"{categories_sheet}!{interest_start}:{interest_end}"

    main()
