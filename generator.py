import shutil
from pathlib import Path
import gspread
import os
import json
import markdown
import time
from pygments.formatters import HtmlFormatter

# Vars
GSHEET_ID = os.environ['GSHEET_ID']
GSHEET_TAB = os.environ['GSHEET_TAB']
SERVICE_ACCOUNT = os.environ['SERVICE_ACCOUNT']
INDEX_PATH = Path("src/template/index-v1.html")

# # create service_account.json
# with open("service_account.json", "w", encoding="utf-8") as f:
#     f.write(SERVICE_ACCOUNT)

# Prepare output folder
dist = Path("dist")
shutil.rmtree(dist, ignore_errors=True)
dist.mkdir(parents=True, exist_ok=True)

# Copy css, img, js
for d in ["css", "img", "js"]:
    src_dir = Path("src") / d
    dst_dir = dist / d
    if src_dir.exists():
        shutil.copytree(src_dir, dst_dir, dirs_exist_ok=True)

# Load credentials and authorize the client
gc = gspread.service_account_from_dict(json.loads(SERVICE_ACCOUNT))

# Open the sheet by ID
sh = gc.open_by_key(GSHEET_ID)

# Select the worksheet by its tab name
worksheet = sh.worksheet(GSHEET_TAB)
# worksheet = sh.worksheet("Sheet4")

# Get all records as a list of dictionaries
data = worksheet.get_all_records()

# Write files
app_version = int(time.time())
post_list = []
blog_description = "Writing What I Might Forget Tomorrow"
blog_name = "Fat Han Nuraddin"
blog_url = "https://fathannuraddin.satu.my.id"
blog_img_default = f"{blog_url}/img/fathan.png"

for row in data:
    path = dist / row['path']
    post_list.append(row.get('home', ''))
    # content = row.get('content', '')

    contentmd = row.get('contentmd', '')
    generated_html = markdown.markdown(
        contentmd, 
        extensions=['fenced_code', 'codehilite'],
        extension_configs={
            'codehilite': {
                'linenums': True,  # Force row numbers on all blocks
                'guess_lang': False,    # Disables guessing if you forget to label a code block
            }
        }
    )

    # --- Light Theme Setup ---
    # Choose a clean light theme (e.g., 'default', 'github', 'tango', or 'vs')
    light_formatter = HtmlFormatter(style="default")
    light_css = light_formatter.get_style_defs('.codehilite')

    # --- Dark Theme Setup ---
    # Choose a clean dark theme (e.g., 'monokai', 'github-dark', 'one-dark', or 'dracula')
    dark_formatter = HtmlFormatter(style="github-dark")
    dark_css = dark_formatter.get_style_defs('.codehilite')

    # --- Combine into a Responsive CSS Block ---
    adaptive_css_theme = f"""
    /* 1. Default fallback / Light Mode styles */
    {light_css}

    /* 2. Automatic Dark Mode Override via Browser Settings */
    @media (prefers-color-scheme: dark) {{
    {dark_css}
    }}
    """

    generated_html_page = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Rendered Markdown</title>
        <style>
            body {{ font-family: sans-serif; padding: 20px; max-width: 800px; margin: 0 auto; }}
            /* Inject the Pygments Colors here */
            {adaptive_css_theme}
        </style>
    </head>
    <body>
        {generated_html}
    </body>
    </html>
    """

    # Create the folder if it doesn't exist
    folder = os.path.dirname(path)
    if folder:
        os.makedirs(folder, exist_ok=True)

    # Create and write the file
    with open(path, "w", encoding="utf-8") as file:
        file.write(generated_html_page)
        print(f"Successfully created: {path}")


# Create and write index file
content_index = ""
with open(INDEX_PATH, "r", encoding="utf-8") as f:
    content_index = f.read()
content_index = content_index.replace("<<app_version>>", str(app_version))
content_index = content_index.replace("<<post_list>>", " ".join(post_list))
content_index = content_index.replace("<<blog_description>>", blog_description)
content_index = content_index.replace("<<blog_name>>", blog_name)
content_index = content_index.replace("<<blog_url>>", blog_url)
content_index = content_index.replace("<<blog_img_default>>", blog_img_default)

with open(dist / "index.html", "w", encoding="utf-8") as file:
    file.write(content_index)
    print(f"Successfully created index")