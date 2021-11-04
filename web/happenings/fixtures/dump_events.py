import json
import os
import sys
import django
from constants import *

### Need to setup django before importing django models ###
sys.path.append(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "web.settings")
django.setup()
####### 

from dotenv import load_dotenv
from googleapiclient.discovery import build
from django.utils import timezone
from happenings.models import InterestCategory, RequirementCategory
from helper import empty_table_in_spreadsheet


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
                    "admin_approved": row[events[0].index("admin_approved")],
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

    events_data = autofill_events(spreadsheet)
    
    with open(f"{PATH}/{EVENTS_FILE}", "w") as output:
        json.dump(events_data, output, indent=4)
        output.write("\n")


if __name__ == '__main__':
    # Configuration: Environment variables
    dotenv_file = os.path.join(BASE_DIR, ".env")
    
    if os.path.isfile(dotenv_file):
        load_dotenv(dotenv_file)

    main()
