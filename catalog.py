import os.path
from typing import List

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from bigbox import fetch_box, Box

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

# The ID and range of a sample spreadsheet.
# SAMPLE_SPREADSHEET_ID = "1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms"
SAMPLE_SPREADSHEET_ID = "1l-9r4ZnABDN1fI4Gwn2u3x1eQ-bAJkCMyekHc_xvhIY"
SAMPLE_RANGE_NAME = "Sheet1!A1:G5"


class Item:
    def __init__(self, url, age_range: str, event_type: str, people_count: str, relationship: str, interests: str, price_range: str):
        self.url = url
        self.age_range = age_range
        self.event_type = event_type
        self.people_count = people_count
        self.relationship = relationship
        self.interests = interests
        self.price_range = price_range


class Catalog:
    def __init__(self):
        self.items: List[Item] = []

    def load_catalog(self):
        """Shows basic usage of the Sheets API.
        Prints values from a sample spreadsheet.
        """
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", SCOPES
                )
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open("token.json", "w") as token:
                token.write(creds.to_json())

        try:
            service = build("sheets", "v4", credentials=creds)

            # Call the Sheets API
            sheet = service.spreadsheets()
            result = (
                sheet.values()
                .get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME)
                .execute()
            )
            values = result.get("values", [])

            if not values:
                print("No data found.")
                return

            header_list = values[0]
            header_position = {header: i for i, header in enumerate(header_list)}

            self.items = [Item(url=row[header_position["url"]],
                         age_range=row[header_position["Rango edad"]],
                         event_type=row[header_position["Tipo Evento"]],
                         people_count=row[header_position["Cant. Personas"]],
                         relationship=row[header_position["Tipo de relación"]],
                         interests=row[header_position["Intereses"]],
                         price_range=row[header_position["Rango de precio"]]) for row in values[1:]]

        except HttpError as err:
            print(err)

    def get_box(self, id) -> Box:
        return fetch_box(id)
