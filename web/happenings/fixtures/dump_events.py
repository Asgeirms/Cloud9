import json
import os

from pathlib import Path
from dotenv import load_dotenv
from googleapiclient.discovery import build
from django.utils import timezone
from django.conf import settings


def main():
    data = []
    pk_counter = 99999

    # Building the service used to call the Sheet API
    service = build('sheets', 'v4', developerKey=API_KEY)
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=event_range).execute()
    events = result.get('values', [])

    if not events:
        raise Exception(f"Spreadsheet {SPREADSHEET_ID} does not contain data at range {event_range}")

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
                    "host": "1"

                    # Skipping categories for now
                    # "interest_categories": row[events[0].index("interest_categories")],
                    # "requirement_categories": row[events[0].index("requirement_categories")],
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
                "start_time": start_time.strftime(('%Y-%m-%dT%H:%M:%SZ')),
                "end_time": end_time.strftime(('%Y-%m-%dT%H:%M:%SZ')),
                "event": event_pk
            }
        }

        data.append(schedule)
    
    with open(f"{path}/{filename}", "w") as output:
        json.dump(data, output, indent=4)
        output.write("\n")

if __name__ == '__main__':
    # Configurations: timezone and environment variables
    settings.configure()

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    dotenv_file = os.path.join(BASE_DIR, ".env")
    
    if os.path.isfile(dotenv_file):
        load_dotenv(dotenv_file)
    
    API_KEY = os.environ['SHEET_KEY']

    path = "happenings/fixtures"
    filename = "events.json"

    # Spreadsheet values in the "Auto fill" data sheet
    SPREADSHEET_ID = "1R7xoCYJUm_pgVj7j80cZBEhBUprw1mPLx069Zz9uYfY"
    event_sheet = "Events"
    event_start = "A1"  
    event_end = "K19"
    event_range = f"{event_sheet}!{event_start}:{event_end}"

    main()
