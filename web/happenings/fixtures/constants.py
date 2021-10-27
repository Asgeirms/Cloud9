import os
from dotenv import load_dotenv

# Configuration: Environment variables
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
dotenv_file = os.path.join(BASE_DIR, ".env")

if os.path.isfile(dotenv_file):
    load_dotenv(dotenv_file)

API_KEY = os.environ['SHEET_KEY']
SPREADSHEET_ID = "1R7xoCYJUm_pgVj7j80cZBEhBUprw1mPLx069Zz9uYfY"
PATH = "happenings/fixtures"

### Events ###
EVENTS_FILE = "events.json"

event_sheet = "Events"
event_start = "A1"  
event_end = "K19"
event_range = f"{event_sheet}!{event_start}:{event_end}"

### Categories ###
CATEGORIES_FILE = "categories.json"

categories_sheet = "Categories"

# Requirements categories
req_start = "A2"
req_end = "B14"
req_range = f"{categories_sheet}!{req_start}:{req_end}"

# Interest categories
interest_start = "E2"
interest_end = "F19"
interest_range = f"{categories_sheet}!{interest_start}:{interest_end}"
