import os
import base64
import json

# Path to the config file
CONFIG_FILE_PATH = './turbosrc-service/.config.json'

# Fetch the base64 encoded environment variable
turbosrc_testers_b64 = os.environ.get("TURBOSRC_TESTERS")

if not turbosrc_testers_b64:
    raise ValueError("TURBOSRC_TESTERS environment variable is not set.")

# Decode base64 content to get the actual JSON data
turbosrc_testers_json = base64.b64decode(turbosrc_testers_b64).decode('utf-8')

# Parse the JSON content
testers_data = json.loads(turbosrc_testers_json)

# Load the existing config file content
with open(CONFIG_FILE_PATH, 'r') as file:
    config_data = json.load(file)

# Replace the testers field in the config data with the new testers data
config_data['testers'] = testers_data

# Save the updated config data back to the file
with open(CONFIG_FILE_PATH, 'w') as file:
    json.dump(config_data, file, indent=4)

print(f"Updated 'testers' field in {CONFIG_FILE_PATH}.")
