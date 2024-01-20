import os
import base64
import glob
import json
import subprocess
import argparse
import requests
import re
import traceback
import sys
import time
import random
import shutil
import errno
from requests.exceptions import ConnectionError

def usage():
    print("Usage: script.py [init USERNAME REPO ACTION]")
    print("  init: initialize necessary files and directories")
    exit(1)

def remove_folder_if_exists(dir_path):
    """
    Remove a folder if it exists, handling permission errors.

    :param dir_path: The path to the directory to be removed.
    """
    def onerror(func, path, exc_info):
        """
        Error handler for shutil.rmtree.
        """
        if not isinstance(exc_info[1], PermissionError):
            sys.exit(f"\n\nPlease run `sudo rm -r gitea`, which is has gitea data.\nOr run ./tsrc-dev with 'sudo' so it has permissions to delete the gitea folder")

    if os.path.exists(dir_path) and os.path.isdir(dir_path):
        try:
            shutil.rmtree(dir_path, onerror=onerror)
            print(f"Removed folder: {dir_path}")
        except PermissionError:
            print(f"Permission denied while removing folder: {dir_path}")
    else:
        print(f"Folder does not exist: {dir_path}")

def create_files(*file_paths):
    """
    Creates empty files at each specified file path.

    :param file_paths: A variable number of file paths where files will be created.
    """
    for file_path in file_paths:
        with open(file_path, 'w') as file:
            # This will create an empty file at each specified path.
            pass

def copy_file_to_directory(src_file, dest_dir):
    """
    Copies a file from src_file to the directory dest_dir.

    :param src_file: The path to the source file.
    :param dest_dir: The path to the destination directory.
    """
    # Check if the destination directory exists, create if not
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    # Copy the file
    shutil.copy(src_file, dest_dir)

def write_env_variables(file_name, variables):
    """
    Writes given environment variables to a .env file.

    :param file_name: The name of the .env file.
    :param variables: A dictionary of environment variables to write.
    """
    with open(file_name, 'w') as file:
        for key, value in variables.items():
            file.write(f"{key}={value}\n")

def populate_gitea_env():
    with open('./turbosrc.config', 'r') as f:
        turbosrcConfigData = json.load(f)
    username = turbosrcConfigData.get('GithubName')
    password = turbosrcConfigData.get('GithubPassword')
    secret = turbosrcConfigData.get('Secret')

    env_variables = {
        "USER_UID": "1000",
        "USER_GID": "1000",
        "GITEA_DB_TYPE": "postgres",
        "GITEA_DB_HOST": "postgres:5432",
        "GITEA_DB_NAME": username,
        "GITEA_DB_USER": username,
        "GITEA_DB_PASSWD": password,
        "INSTALL_LOCK": "true",
        "SECRET_KEY": secret,
        "DISABLE_REGISTRATION": "true",
        "REQUIRE_SIGNIN_VIEW": "true",
        "POSTGRES_USER": username,
        "POSTGRES_PASSWORD": password,
        "POSTGRES_DB": username
    }

    write_env_variables('.gitea.env', env_variables)

def local_add_testers():
    # Path to the config file
    CONFIG_FILE_PATH = './turbosrc-service/.config.json'

    # Path to the file containing the data
    DATA_FILE_PATH = '.tester_fields_for_turbosrc_service.json'

    # Read the data from the file
    with open(DATA_FILE_PATH, 'r') as file:
        tester_json = file.read()

    # Parse the JSON content
    testers_data = json.loads(tester_json)

    # Load the existing config file content
    with open(CONFIG_FILE_PATH, 'r') as file:
        config_data = json.load(file)

    # Replace the testers field in the config data with the new testers data
    config_data['testers'] = testers_data

    # Save the updated config data back to the file
    with open(CONFIG_FILE_PATH, 'w') as file:
        json.dump(config_data, file, indent=4)

    print(f"Updated 'testers' field in {CONFIG_FILE_PATH}.")

def remove_files(file_paths):
    for file_path in file_paths:
        # Expand wildcard patterns, if any
        expanded_paths = glob.glob(file_path)

        for path in expanded_paths:
            # Check if file exists to prevent errors
            if os.path.exists(path):
                try:
                    os.remove(path)
                    print(f"Removed: {path}")
                except Exception as e:
                    print(f"Error removing {path}: {e}")
            else:
                print(f"File not found: {path}")

def initialize_files():
    with open('./turbosrc.config', 'r') as f:
        config_data = json.load(f)

    USER = config_data.get('GithubName', None)
    GITHUB_API_TOKEN = config_data.get('GithubApiToken', None)
    SECRET = config_data.get('Secret', None)
    ADDR = config_data.get('TurboSrcID', None)
    MODE = config_data.get('Mode', None)

    if ADDR:
        if not is_valid_ethereum_address(ADDR):
            ADDR = None
    else:
        ADDR = None

    if MODE in ['local', 'router-host']:
        URL = "http://turbosrc-service:4000/graphql"
    elif MODE in ['router-client', 'online']:
        URL = ""

    # Check each variable individually and raise an error with specific message
    if USER is None:
        raise ValueError("Failed to initialize files: GithubName not found in turbosrc.config")
    if GITHUB_API_TOKEN is None:
        raise ValueError("Failed to initialize files: GithubApiToken not found in turbosrc.config")
    if SECRET is None and MODE != 'online':
        raise ValueError("Failed to initialize files: Secret not found in turbosrc.config")
    if MODE is None:
        raise ValueError("Failed to initialize files: Mode not found in turbosrc.config")

    os.makedirs('./GihtubMakerTools', exist_ok=True)
    os.makedirs('./fork-repo', exist_ok=True)
    os.makedirs('./create_pull_requests', exist_ok=True)
    os.makedirs('./turbosrc-service', exist_ok=True)

    with open('./GihtubMakerTools/ght.ini', 'w') as f:
        f.write(f"[github.org]\nUser = {USER}\nToken = {GITHUB_API_TOKEN}\nOrganization =")

    with open('./fork-repo/env.list', 'w') as f:
        f.write(f"GITHUB_TOKEN={GITHUB_API_TOKEN}")

    with open('./create_pull_requests/env.list', 'w') as f:
        f.write(f"GITHUB_TOKEN={GITHUB_API_TOKEN}")

    config = {
        "github": {
            "organization": "turbo-src",
            "user": USER,
            "apiToken": GITHUB_API_TOKEN
        },
        "turbosrc": {
            "endpoint": {
              "mode": "online",
              "url": URL,
              "egressURLoption": URL
            },
            "jwt": SECRET,
            "store": {
                "repo": {
                    "addr": "REPO_ADDR",
                    "key": "REPO_KEY"
                },
                "contributor": {
                    "addr": ADDR,
                    "key": "YOUR_KEY"
                }
            }
        },
        "offchain": {
            "endpoint": {
                "mode": "online",
                "url": "http://turbosrc-engine:4002/graphql"
            }
        },
        "namespace": {
            "endpoint": {
                "mode": "online",
                "url": "http://namespace-service:4003/graphql"
            }
        },
        "gh": {
            "endpoint": {
                "mode": "online",
                "url": "http://gh-service:4004/graphql"
            }
        },
        "testers": {}
    }

    with open('./turbosrc-service/.config.json', 'w') as f:
        json.dump(config, f, indent=4)

    return MODE

def update_api_token():
    with open('./turbosrc-service/.config.json', 'r') as f:
        data = json.load(f)

    apiToken = data['github']['apiToken']

    with open('./turbosrc.config', 'r') as f:
        turbosrcConfigData = json.load(f)
    with open('./turbosrc-service/.config.json', 'r') as f:
        serviceConfigData = json.load(f)

    secret = turbosrcConfigData.get('Secret')
    mode = turbosrcConfigData.get('Mode')
    if secret is None and mode == 'online':
       secret = 'noSecretNeededInOnlineModeThisIsAplaceholder'

    decryptedToken = subprocess.check_output([
        'docker-compose', 'run', '--rm', 'jwt_hash_decrypt', '--secret=' + secret, '--string={\"githubToken\": \"' + apiToken + '\"}'
    ]).decode('utf-8').split('\n')[-2]

    serviceConfigData['github']['apiToken'] = decryptedToken

    with open('./turbosrc-service/.config.json', 'w') as f:
        json.dump(serviceConfigData, f, indent=4)

def is_valid_ethereum_address(address):
    try:
        return bool(re.match("^0x[a-fA-F0-9]{40}$", address))
    except Exception as e:
        print(f"Failed to check if provided string is a valid Ethereum address. Error: {str(e)}")
        traceback.print_exc()
        return False

def find_or_create_user_from_config():
    try:
        with open('./turbosrc-service/.config.json', 'r') as f:
            data = json.load(f)

        url = 'http://localhost:4003'  # data['namespace']['endpoint']['url']
        token = data['github']['apiToken']
        contributor_name = data['github']['user']

        contributor_id, contributor_signature = find_or_create_user(contributor_id=None, contributor_name=None, contributor_signature=None, token=token)

        return (contributor_id, contributor_signature)
    except Exception as e:
        print(f"Failed to get contributor id. Error: {str(e)}")
        traceback.print_exc()
        return None

def update_contributor_id(contributor_id, contributor_signature):
    try:
        with open('./turbosrc-service/.config.json', 'r') as f:
            data = json.load(f)

        data['turbosrc']['store']['contributor']['key'] = contributor_signature

        current_address = data['turbosrc']['store']['contributor']['addr']

        #if not is_valid_ethereum_address(current_address):
        data['turbosrc']['store']['contributor']['addr'] = contributor_id

        with open('./turbosrc-service/.config.json', 'w') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"Failed to update contributor id. Error: {str(e)}")
        traceback.print_exc()

def manage_docker_service(service, command):
    if command == 'up':
      subprocess.run(['docker-compose', command, '-d', service], check=True)
    elif command == 'build':
      subprocess.run(['docker-compose', command, service], check=True)
    elif command == 'stop':
        subprocess.run(['docker-compose', command, service], check=True)

def configure_namespace_data_docker(action):
    if action == 'start':
        manage_docker_service('namespace-service', 'up')
        max_retries = 30  # maximum attempts to check if the service is up
        retries = 0
        last_error = None
        while retries < max_retries:
            try:
                with open('./turbosrc.config', 'r') as f:
                    config_data = json.load(f)

                contributor_name_config = config_data.get('GithubName', None)
                token = config_data.get('GithubApiToken', None)
                contributor_id_config = config_data.get('TurboSrcID', None)
                contributor_signature_config = config_data.get('TurboSrcKey', None)
                MODE = config_data.get('Mode', None)

                url = 'http://localhost:4003'  # data['namespace']['endpoint']['url']

                # Try to fetch contributor id and signature rom turbosrc.config
                contributor_id = get_contributor_id(contributor_name_config)
                contributor_signature = get_contributor_signature(contributor_id)

                contributor_name = contributor_name_config

                # Namespace service unfortunately returns "none" instead of None, if not found,
                # so normalize here.
                if contributor_id == "none":
                    contributor_id = None
                if contributor_signature == "none":
                    contributor_signature = None

                if contributor_id_config == "":
                   contributor_id_config = None
                if contributor_signature_config == "":
                    contributor_signature_config = None

                if contributor_id_config is not None and contributor_signature_config is not None:
                    print("\nFound TurboSrcID and TurboSrcKey in config!\n")
                    contributor_id, contributor_signature = find_or_create_user(contributor_id_config, contributor_name, contributor_signature=contributor_signature_config, token=token)
                    update_turbosrc_config(turboSrcID=contributor_id_config, turboSrcKey=contributor_signature_config)
                    update_contributor_id(contributor_id_config, contributor_signature_config)
                    break

                # Create user if not found
                if contributor_id is None and contributor_signature is None:
                    print("\nCreating TurboSrcID and TurboSrcKey\n")
                    #if contributor_id_config is not None and contributor_signature_config is not None:
                    #    contributor_id = contributor_id_config
                    #    contributor_signature = contributor_signature_config
                    if contributor_signature is None:
                        contributor_signature = "none"
                    contributor_id, contributor_signature = find_or_create_user(contributor_id, contributor_name, contributor_signature, token=token)

                    update_turbosrc_config(turboSrcID=contributor_id, turboSrcKey=contributor_signature)
                    update_contributor_id(contributor_id, contributor_signature)
                    break
            except ConnectionError as e:
                last_error = e
                # If a connection error occurred, sleep for a while and try again
                time.sleep(2)
                retries += 1
        else:
            # If the loop has exhausted the max_retries without success, print error message and exit
            if last_error is not None:
                print(f"Failed to fetch contributor id. Error: {str(last_error)}. Exiting...")
                sys.exit(1)
    elif action == 'stop':
        manage_docker_service('namespace-service', 'stop')

def update_turbosrc_id_egress_router_url_in_env_file(env_file_path):
    # load turbosrc.store.contributor from .config.json
    with open('./turbosrc-service/.config.json', 'r') as f:
        service_config_data = json.load(f)

    turbosrc_id = service_config_data.get('turbosrc', {}).get('store', {}).get('contributor', {}).get('addr', None)
    turbosrc_key = service_config_data.get('turbosrc', {}).get('store', {}).get('contributor', {}).get('key', None)
    if turbosrc_id is None:
        raise ValueError("'turbosrc.store.contributor.addr' not found in turbosrc-service/.config.json")
    if turbosrc_key is None:
        raise ValueError("'turbosrc.store.contributor.key' not found in turbosrc-service/.config.json")

    egress_router_url = service_config_data.get('turbosrc', {}).get('endpoint', {}).get('egressURLoption', None)
    if egress_router_url is None:
        raise ValueError("'turbosrc.turbosrc.endpoint' not found in turbosrc-service/.config.json")

    # Read the original lines from the file
    with open(env_file_path, 'r') as f:
        original_lines = f.readlines()

    # Prepare the updated lines
    updated_lines = []
    found_turbosrc_id = False
    found_turbosrc_key = False
    found_egress_router_url = False
    for line in original_lines:
        if line.startswith('TURBOSRC_ID'):
            line = f"TURBOSRC_ID={turbosrc_id}\n"
            found_turbosrc_id = True
        if line.startswith('TURBOSRC_KEY'):
            line = f"TURBOSRC_KEY={turbosrc_key}\n"
            found_turbosrc_key = True
        if line.startswith('EGRESS_ROUTER_URL'):
            line = f"EGRESS_ROUTER_URL={egress_router_url}\n"
            found_egress_router_url = True
        updated_lines.append(line)

    # If we didn't find a TURBOSRC_ID line, append one
    if not found_turbosrc_id:
        updated_lines.append(f"TURBOSRC_ID={turbosrc_id}\n")
    if not found_turbosrc_key:
        updated_lines.append(f"TURBOSRC_KEY={turbosrc_key}\n")
    if not found_egress_router_url:
        updated_lines.append(f"EGRESS_ROUTER_URL={egress_router_url}\n")

    # Write the updated lines back to the file
    with open(env_file_path, 'w') as f:
        f.writelines(updated_lines)

def check_and_create_service_env(env_file_path):
    # Check if the service.env file exists
    if not os.path.exists(env_file_path):
        # If not, create an empty file
        open(env_file_path, 'a').close()

def validate_and_update_endpoint_url():
    with open('./turbosrc.config', 'r') as f:
        config_data = json.load(f)

    mode = config_data.get('Mode', None)

    if mode is not None:
        with open('./turbosrc-service/.config.json', 'r') as f:
            service_config_data = json.load(f)

        service_config_data['turbosrc']['endpoint']['egressURLoption'] = "http://turbosrc-egress-router:4006/graphql"

        if mode in ['local', 'router-host']:
            service_config_data['turbosrc']['endpoint']['url'] = "http://turbosrc-service:4000/graphql"

        if mode == 'router-client':
            service_config_data['turbosrc']['endpoint']['url'] = "http://turbosrc-service:4000/graphql"

        with open('./turbosrc-service/.config.json', 'w') as f:
            json.dump(service_config_data, f, indent=4)

    else:
        raise ValueError("Missing 'Mode' value in 'turbosrc.config'")

def remove_egressURLoption():
    with open('./turbosrc-service/.config.json', 'r') as f:
        config = json.load(f)

    if config.get('turbosrc', {}).get('endpoint', {}).get('egressURLoption', None) is not None:
        del config['turbosrc']['endpoint']['egressURLoption']

        with open('./turbosrc-service/.config.json', 'w') as f:
            json.dump(config, f, indent=4)

def update_egressURLoption():
    with open('./turbosrc-service/.config.json', 'r') as f:
        config = json.load(f)

    if config.get('turbosrc', {}).get('endpoint', {}).get('egressURLoption', None) is not None:
        config['turbosrc']['endpoint']['egressURLoption'] = "https://turbosrc-marialis.dev"

        with open('./turbosrc-service/.config.json', 'w') as f:
            json.dump(config, f, indent=4)

def update_turbosrc_url(url):
    with open('./turbosrc-service/.config.json', 'r') as f:
        config = json.load(f)

    if config.get('turbosrc', {}).get('endpoint', {}).get('url', None) is not None:
        config['turbosrc']['endpoint']['url'] = url
        with open('./turbosrc-service/.config.json', 'w') as f:
            json.dump(config, f, indent=4)

def create_chrome_extension_config_files():
    # Define the directory and file names
    directory = "./chrome-extension"
    filenames = ["config.devOnline.json", "config.devLocal.json", "config.devRouter.json"]

    # Ensure the directory exists
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Loop through each file and create it if it doesn't exist
    for filename in filenames:
        file_path = os.path.join(directory, filename)
        if not os.path.exists(file_path):
            with open(file_path, 'w') as file:
                file.write("{}")  # Write an empty JSON object

    print("Chrome extension config files created.")

def add_or_update_current_version(path):
    # Load the existing Chrome extension config data from file
    with open(path, 'r') as f:
        chrome_extension_config = json.load(f)

    # Get the latest commit SHA for the currentVersion attribute
    commit_sha = get_latest_commit_sha()

    if not commit_sha:
        print("Failed to get the latest commit SHA. `currentVersion` will not be updated.")
        return

    # Add or update the currentVersion field in the Chrome extension config
    chrome_extension_config["currentVersion"] = commit_sha

    # Save the updated data back to the file
    with open(path, 'w') as f:
        json.dump(chrome_extension_config, f, indent=4)
        print(f"Updated {path} with the latest commit SHA: {commit_sha}")

def update_chrome_extension_config():
    # Load turbosrc_config_data from ./turbosrc-service/.config.json
    with open('./turbosrc-service/.config.json', 'r') as f:
        turbosrc_config_data = json.load(f)

    # Create the initial Chrome extension config data
    chrome_extension_config = {
        "url": "https://turbosrc-marialis.dev",
        "myTurboSrcID": turbosrc_config_data['turbosrc']['store']['contributor']['addr'],
        "myGithubName": turbosrc_config_data['github']['user'],
    }

    # Save the data back to ./chrome-extension/config.devOnline.json
    with open('./chrome-extension/config.devOnline.json', 'w') as f:
        json.dump(chrome_extension_config, f, indent=4)

def update_chrome_extension_config_online():
    # Load turbosrc_config_data from ./turbosrc-service/.config.json
    with open('./turbosrc-service/.config.json', 'r') as f:
        turbosrc_config_data = json.load(f)

    # Create the initial Chrome extension config data
    chrome_extension_config = {
        "url": "https://turbosrc-marialis.dev",
    }

    # Save the data back to ./chrome-extension/config.devOnline.json
    with open('./chrome-extension/config.devOnline.json', 'w') as f:
        json.dump(chrome_extension_config, f, indent=4)

def update_chrome_extension_config_local(visual):
    # Create the initial Chrome extension config data
    if visual is True:
      # For local testing purposes to overcome ssl issues between viatui graphical tester
      # and locally served turbosrc.
      chrome_extension_config = {
          "url": "http://ssl-proxy:8080/graphql"
      }
    else:
      chrome_extension_config = {
          "url": "http://localhost:4000/graphql"
      }

    # Save the data back to ./chrome-extension/config.devOnline.json
    with open('./chrome-extension/config.devLocal.json', 'w') as f:
        json.dump(chrome_extension_config, f, indent=4)

def query_graphql(query):
    last_exception = None
    max_retries = 5
    try:
        with open('./turbosrc-service/.config.json', 'r') as f:
            data = json.load(f)

        url = 'http://localhost:4003'  # data['namespace']['endpoint']['url']

        for i in range(max_retries):
            try:
                response = requests.post(f"{url}/graphql", json={'query': query}, headers={"Content-Type": "application/json", "Accept": "application/json"})
                if response.status_code != 200:
                    print(response.text)
                response.raise_for_status()
                result = response.json()
                if 'data' in result:
                    return result['data']
            except Exception as e:
                last_exception = e
                if i < max_retries - 1:  # if not the last attempt, skip to the next iteration
                    # exponential backoff with jitter
                    wait_time = (2 ** i) + random.random()
                    time.sleep(wait_time)
                    continue
                else:  # if this is the last attempt, then raise the exception
                    raise last_exception
    except Exception as e:
        print(f"Error during GraphQL query: {str(e)}")
        traceback.print_exc()
        return None

def find_or_create_user(contributor_id=None, contributor_name=None, contributor_signature="none", token=None):
    try:
        query = f"""
        {{
            findOrCreateUser(owner: "", repo: "", contributor_id: "{contributor_id}", contributor_name: "{contributor_name}", contributor_signature: "{contributor_signature}", token: "{token}") {{
                contributor_name,
                contributor_id,
                contributor_signature,
                token
            }}
        }}
        """

        result = query_graphql(query)
        if result and result.get('findOrCreateUser'):
            return (result['findOrCreateUser']['contributor_id'], result['findOrCreateUser']['contributor_signature'])
        else:
            #print(f"Unexpected result format: {result}")
            return None, None

    except Exception as e:
        print(f"Failed to find or create user. Error: {str(e)}")
        traceback.print_exc()
        return None, None

def get_contributor_name(contributor_id):
    query = f"""
    {{
        getContributorName(owner: "", repo: "", defaultHash: "", contributor_id: "{contributor_id}")
    }}
    """

    result = query_graphql(query)
    if result and result.get('getContributorName'):
        return result['getContributorName']['contributor_name']

    return None

def get_contributor_id(contributor_name):
    query = f"""
    {{
        getContributorID(owner: "", repo: "", defaultHash: "", contributor_name: "{contributor_name}")
    }}
    """

    result = query_graphql(query)

    if isinstance(result, str):
        return result  # It's already the ID or error message.
    else:
        #print(f"Unexpected result format: {result}")
        return None

def get_contributor_signature(contributor_id):
    query = f"""
    {{
        getContributorSignature(owner: "", repo: "", defaultHash: "", contributor_id: "{contributor_id}")
    }}
    """

    result = query_graphql(query)

    # If 'getContributorSignature' is present in the result and its value is a dictionary
    if isinstance(result, dict) and 'getContributorSignature' in result:
        # Check if the result is a string, e.g., "none"
        if isinstance(result['getContributorSignature'], str):
            #print(f"Unexpected contributor signature format: {result['getContributorSignature']}")
            return None

        # If the result is structured as expected, return the signature
        return result['getContributorSignature']

    else:
        #print(f"Unexpected result format: {result}")
        return None

def update_turbosrc_config(turboSrcID=None, turboSrcKey=None):
    """
    Updates the TurboSrcID or TurboSrcKey in turbosrc.config based on passed values.

    :param turboSrcID: New value for TurboSrcID. If None, it won't be updated.
    :param turboSrcKey: New value for TurboSrcKey. If None, it won't be updated.
    :return: None
    """

    # Load existing data from config
    with open('./turbosrc.config', 'r') as f:
        config_data = json.load(f)

    # Update the values if they are provided
    if turboSrcID:
        config_data['TurboSrcID'] = turboSrcID

    if turboSrcKey:
        config_data['TurboSrcKey'] = turboSrcKey

    # Save updated data back to config
    with open('./turbosrc.config', 'w') as f:
        json.dump(config_data, f, indent=4)

def get_latest_commit_sha():
    """
    Get the latest commit SHA from git.

    Returns:
        str: The latest commit SHA.
        None: If there was an error fetching the commit SHA.
    """
    try:
        commit_sha = subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode('utf-8').strip()
        return commit_sha
    except subprocess.CalledProcessError:
        print("Error fetching the latest commit SHA from git.")
        return None


def update_version_ingress_service_env():
    # Navigate to the specified directory (can be changed)
    os.chdir('./')

    commit_sha = get_latest_commit_sha()
    if not commit_sha:
        return

    # File path
    file_path = './turbosrc-ingress-router/service.env'

    # Check if the file exists
    if not os.path.exists(file_path):
        print(f"'{file_path}' does not exist.")
        return

    # Read the content of the file
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Check if the CURRENT_VERSION line exists
    found = any(line.startswith('CURRENT_VERSION=') for line in lines)

    # Update or append the CURRENT_VERSION line
    with open(file_path, 'w') as file:
        if found:
            for line in lines:
                if line.startswith('CURRENT_VERSION='):
                    file.write(f'CURRENT_VERSION={commit_sha}\n')
                else:
                    file.write(line)
        else:
            # If the line was not found, append it to the end of the file
            lines.append(f'CURRENT_VERSION={commit_sha}\n')
            file.writelines(lines)

    # Validate that the operation succeeded
    with open(file_path, 'r') as file:
        if any(line == f'CURRENT_VERSION={commit_sha}\n' for line in file.readlines()):
            print(f"Updated {file_path} with the latest commit SHA: {commit_sha}")
        else:
            print(f"Failed to update {file_path}")

def update_version_egress_service_env():
    # Navigate to the specified directory (can be changed)
    os.chdir('./')

    commit_sha = get_latest_commit_sha()
    if not commit_sha:
        return

    # File path
    file_path = './turbosrc-egress-router/service.env'

    # Check if the file exists
    if not os.path.exists(file_path):
        print(f"'{file_path}' does not exist.")
        return

    # Read the content of the file
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Check if the CURRENT_VERSION line exists
    found = any(line.startswith('COMPATIBLE_VERSIONS=') for line in lines)

    # Update or append the CURRENT_VERSION line
    with open(file_path, 'w') as file:
        if found:
            for line in lines:
                if line.startswith('COMPATIBLE_VERSIONS='):
                    file.write(f'COMPATIBLE_VERSIONS=["{commit_sha}"]\n')
                else:
                    file.write(line)
        else:
            # If the line was not found, append it to the end of the file
            lines.append(f'COMPATIBLE_VERSIONS=["{commit_sha}"]\n')
            file.writelines(lines)

    # Validate that the operation succeeded
    with open(file_path, 'r') as file:
        if any(line == f'COMPATIBLE_VERSIONS=["{commit_sha}"]\n' for line in file.readlines()):
            print(f"Updated {file_path} with the latest commit SHA: {commit_sha}")
        else:
            print(f"Failed to update {file_path}")

def copy_chrome_extension_to_viatui():
    source_dir = './chrome-extension/dist'
    dest_dir = './viatui/dist-chrome-extension'
    print(f"Copying {source_dir} to {dest_dir}")

    # Check if source directory exists
    if not os.path.exists(source_dir):
        print(f"{source_dir} does not exist:", source_dir)
        return

    # Delete the destination directory, if it exists
    try:
        # Delete the destination directory if it exists
        shutil.rmtree(dest_dir)
        print(f"viatui's {dest_dir} directory exists already, and it was deleted successfully.")

    except Exception as e:
        print("An error occurred:", e)

    # Copy the entire directory
    try:
        shutil.copytree(source_dir, dest_dir, dirs_exist_ok=True)
        print("Copy of dist for viatui completed successfully.")
    except Exception as e:
        print("An error occurred:", e)

def create_chrome_extension_dist_directory():
    dir_path = './chrome-extension/dist'

    # Check if the directory exists
    if os.path.exists(dir_path):
        # If it exists, delete it
        shutil.rmtree(dir_path)
        print("Existing directory removed:", dir_path)

    # Create the directory
    os.makedirs(dir_path)
    print("Directory created:", dir_path)

def create_viatui_screenshot_directory():
    dir_path = './viatui/chromium-nix-screenshots'

    # Check if the directory exists
    if os.path.exists(dir_path):
        # If it exists, delete it
        shutil.rmtree(dir_path)
        print("Existing directory removed:", dir_path)

    # Create the directory
    os.makedirs(dir_path)
    print("Directory created:", dir_path)

def create_and_update_viatuix_json():
    viatuix_json_path = './viatui/viatuix.json'
    config_path = './turbosrc.config'

    # Step 1: Create viatuix.json with {}
    with open(viatuix_json_path, 'w') as file:
        json.dump({}, file)

    # Step 2: Read GitHub credentials from turbosrc.config
    if os.path.exists(config_path):
        with open(config_path, 'r') as file:
            config_data = json.load(file)
            github_name = config_data.get('GithubName')
            github_password = config_data.get('GithubPassword')

            if not github_name or not github_password:
                print("Github credentials not found in config.")
                return

            # Step 3: Update viatuix.json with additional details
            data = {
                "username": github_name,
                "password": github_password,
                "url1": "github.com/",
                "url2": "github.com/login",
                "url3": f"github.com/{github_name}/demo/pulls"
            }

            with open(viatuix_json_path, 'w') as file:
                json.dump(data, file, indent=4)

            print("viatuix.json updated successfully.")
    else:
        print("Config file not found:", config_path)

def git_checkout_pull_request(branch_name, repo_dir):
    """
    Fetches the specified branch from the remote origin and checks it out in the specified repository directory.
    """
    try:
        # Fetch the specified branch from the remote and create a local branch
        subprocess.run(['git', 'fetch', '--depth', '1', 'origin', f'{branch_name}:{branch_name}'], check=True, cwd=repo_dir)

        # Checkout the specified branch
        subprocess.run(['git', 'checkout', branch_name], check=True, cwd=repo_dir)

        print(f"Checked out branch {branch_name} in {repo_dir}")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")

def create_gitea_admin_user():
    # Load configuration data
    with open('./turbosrc.config', 'r') as f:
        turbosrcConfigData = json.load(f)
    username = turbosrcConfigData.get('GithubName')
    password = turbosrcConfigData.get('GithubPassword')
    email = 'turbosrc@turbosrc-marialis.dev'

    # Keep trying the command until it succeeds
    while True:
        try:
            subprocess.run(
                ['docker-compose',
                 'exec',
                 '-T',  # Disable pseudo-tty allocation
                 '-u', 'git',
                 'gitea',  # Service name as defined in docker-compose.yml
                 'gitea',
                 'admin',
                 'user',
                 'create',
                 '--username', username,
                 '--password', password,
                 '--email', email,
                 '--admin',
                 '-c', '/data/gitea/conf/app.ini'],
                check=True
            )
            print("Gitea admin user created successfully.")
            break  # Exit loop if command is successful
        except subprocess.CalledProcessError as e:
            print(f"Command failed. Gitea may not be ready. Retrying in 1 second...")
            time.sleep(1)  # Wait for 1 second before retrying

parser = argparse.ArgumentParser()
parser.add_argument("operation", help="Operation to perform: 'init' initializes necessary files and directories")
parser.add_argument('--testers', action='store_true',
                    help='Flag to indicate adding testers in .tester_fields_for_turbosrc_service.json into turbosrc-service config.')
parser.add_argument('--visual', action='store_true',
                    help='Flag to indicate running visual graphical tester.')
parser.add_argument('--github-actions', action='store_true',
                    help='Flag to indicate running under GitHub Actions')

args = parser.parse_args

if __name__ == "__main__":
    args = parser.parse_args()
    if args.operation.lower() == 'init':

        # Otherwise, ref to branches can't be found.
        git_checkout_pull_request("pullRequest6", "./demo")
        git_checkout_pull_request("pullRequest6ConflictResolved", "./demo")
        git_checkout_pull_request("master", "./demo")

        config_files_to_remove = [
            "turbosrc-service/.config.json",
            "fork-repo/env.list",
            "create_pull_requests/env.list",
            "GihtubMakerTools/ght.ini",
            "turbosrc-ingress-router/service.env",
            "turbosrc-egress-router/service.env",
            "chrome-extension/cypress.env.json",
            "chrome-extension/config.dev*",  # Handles wildcard characters
            "chrome-extension/src/config.js",
            ".gitea.env",
            "git-service/turbosrc.config"
            "viatui/viatuix.json"
        ]
        remove_files(config_files_to_remove)
        remove_folder_if_exists('./gitea/')
        create_chrome_extension_dist_directory()
        create_chrome_extension_config_files()
        # upfront or docker-compose commands fail.
        check_and_create_service_env('./turbosrc-ingress-router/service.env')
        check_and_create_service_env('./turbosrc-egress-router/service.env')
        create_files('.gitea.env')
        populate_gitea_env()

        MODE = initialize_files()
        update_api_token()
        print('Getting or generating user info from namespace subsystem...')
        configure_namespace_data_docker('start')
        configure_namespace_data_docker('stop')
        validate_and_update_endpoint_url()
        update_turbosrc_id_egress_router_url_in_env_file('./turbosrc-ingress-router/service.env')
        update_turbosrc_id_egress_router_url_in_env_file('./turbosrc-egress-router/service.env')
        if MODE != 'router-client':
            remove_egressURLoption()
        if MODE == 'router-client':
            update_egressURLoption()
            update_turbosrc_id_egress_router_url_in_env_file('./turbosrc-ingress-router/service.env')
            update_chrome_extension_config()
            update_version_ingress_service_env()
            add_or_update_current_version('./chrome-extension/config.devOnline.json')
        if MODE == 'router-host':
            update_turbosrc_url("http://turbosrc-egress-router:4006/graphql")
            update_chrome_extension_config()
            update_version_ingress_service_env()
            add_or_update_current_version('./chrome-extension/config.devOnline.json')
        if MODE == 'online':
            update_chrome_extension_config_online()
            add_or_update_current_version('./chrome-extension/config.devOnline.json')
        if MODE == 'local':
            visual = False
            if args.visual:
                visual = True
            update_version_ingress_service_env()
            update_chrome_extension_config_local(visual)
            add_or_update_current_version('./chrome-extension/config.devLocal.json')
        update_version_egress_service_env()
        # Run local_add_testers() only if --github-actions flag is not set and --testers is.
        if args.testers and not args.github_actions:
            local_add_testers()

        ''

        print('Build viatui')
        subprocess.run(['docker-compose', 'build', 'viatui'], check=True)

        print('Build chrome-extension')
        subprocess.run(['docker-compose', 'build', 'chrome-extension'], check=True)
        if MODE == 'local' and visual and not args.github_actions:
            subprocess.run(['docker-compose', 'run', 'chrome-extension', 'yarn', 'devLocal'], check=True)
            copy_chrome_extension_to_viatui()
            create_viatui_screenshot_directory()
            create_and_update_viatuix_json()
        elif MODE != 'local' and not args.github_actions:
          subprocess.run(['docker-compose', 'run', 'chrome-extension', 'yarn', 'devOnline'], check=True)

        print('Configure git-service (copying turbosrc.config into git-service)')
        copy_file_to_directory('./turbosrc.config', './git-service/')

        print(f"Building gitea, just in case, but likely unecessary.")
        manage_docker_service('gitea', 'build')
        print('Setting gitea admin user and password.')
        manage_docker_service('gitea', 'up')
        # give the database a moment to boot and to unlock due to write transations.
        time.sleep(5)
        create_gitea_admin_user()

    else:
        usage()
