import shutil
from pathlib import Path
import gspread
import os
import json

# Vars
GSHEET_ID = os.environ['GSHEET_ID']
GSHEET_TAB = os.environ['GSHEET_TAB']
SERVICE_ACCOUNT = os.environ['SERVICE_ACCOUNT']

# # create service_account.json
# with open("service_account.json", "w", encoding="utf-8") as f:
#     f.write(SERVICE_ACCOUNT)

# Prepare output folder
dist = Path("dist")
shutil.rmtree(dist, ignore_errors=True)
dist.mkdir(parents=True, exist_ok=True)


# Load credentials and authorize the client
gc = gspread.service_account_from_dict(json.load(SERVICE_ACCOUNT))

# Open the sheet by ID
sh = gc.open_by_key(GSHEET_ID)

# Select the worksheet by its tab name
worksheet = sh.worksheet(GSHEET_TAB)

# Get all records as a list of dictionaries
data = worksheet.get_all_records()

# Write files
for row in data:
    path = dist / row['path']
    content = row.get('content', '')

    # Create the folder if it doesn't exist
    folder = os.path.dirname(path)
    if folder:
        os.makedirs(folder, exist_ok=True)

    # Create and write the file
    with open(path, "w") as file:
        file.write(content)
        print(f"Successfully created: {path}")

