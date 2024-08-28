import requests
import re
import json

# URL to fetch
url = "https://www.e-solat.gov.my/index.php?siteId=24&pageId=24"

# Fetching the content
response = requests.get(url, verify=False)
response.raise_for_status()  # Will raise an HTTPError for bad responses

# Get the HTML content
html_content = response.text

# Define patterns
pattern_select = r'<select id="inputZone" class="form-control">([\s\S]*?)</select>'
pattern_optgroup = r'<optgroup([\s\S]*?)</optgroup>'
pattern_state = r'label="([\s\S]*?)"'
pattern_option = r'<option([\s\S]*?)</option>'
pattern_zone_code = r"value='([\s\S]*?)'"

# Extract <select> content
match_select = re.search(pattern_select, html_content)
if match_select:
    select_content = match_select.group(1)
else:
    raise ValueError("Could not find the select element in the HTML content.")

# Extract <optgroup> contents
matches_optgroup = re.findall(pattern_optgroup, select_content)
state_json = {}

for options in matches_optgroup:
    # Extract state name
    match_state = re.search(pattern_state, options)
    if match_state:
        state = match_state.group(1)
        print(f"<h3>{state}</h3>")
    else:
        continue  # Skip if no state found
    
    # Extract zone options
    matches_option = re.findall(pattern_option, options)
    zone_json = {}

    for zone_option in matches_option:
        # Extract zone code
        match_zone_code = re.search(pattern_zone_code, zone_option)
        if match_zone_code:
            zone_code = match_zone_code.group(1)
            zone_name = re.sub(r'<[^>]+>', '', zone_option).split(' - ')[1]
            print(f"{zone_code} : {zone_name}<br>")
            zone_json[zone_code] = zone_name

    state_json[state] = zone_json

# Output JSON
with open("./zone.json", "w") as json_file:
    json.dump(state_json, json_file, indent=4)
