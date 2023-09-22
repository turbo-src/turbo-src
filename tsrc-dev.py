import os
import json
import subprocess
import argparse
import requests
import re
import traceback
import sys
import time
import random
from requests.exceptions import ConnectionError

def usage():
    print("Usage: script.py [init USERNAME REPO ACTION]")
    print("  init: initialize necessary files and directories")
    exit(1)

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
    elif MODE == 'router-client':
        URL = ""

    if None in (USER, GITHUB_API_TOKEN, SECRET, MODE):
        raise ValueError("Failed to initialize files: not all required parameters found in turbosrc.config")

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

def manage_docker_service(action):
    if action == 'start':
        subprocess.run(['docker-compose', 'up', '-d', 'namespace-service'], check=True)
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
        subprocess.run(['docker-compose', 'stop', 'namespace-service'], check=True)

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

def update_chrome_extension_config():
    # Load turbosrc_config_data from ./turbosrc-service/.config.json
    with open('./turbosrc-service/.config.json', 'r') as f:
        turbosrc_config_data = json.load(f)

    # Create or update the Chrome extension config data
    chrome_extension_config = {
        "url": "https://turbosrc-marialis.dev",
        "myTurboSrcID": turbosrc_config_data['turbosrc']['store']['contributor']['addr'],
        "myGithubName": turbosrc_config_data['github']['user']
    }

    # Save the data back to ./chrome-extension/config.devOnline.json
    with open('./chrome-extension/config.devOnline.json', 'w') as f:
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
            print(f"Unexpected result format: {result}")
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
        print(f"Unexpected result format: {result}")
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
            print(f"Unexpected contributor signature format: {result['getContributorSignature']}")
            return None

        # If the result is structured as expected, return the signature
        return result['getContributorSignature']

    else:
        print(f"Unexpected result format: {result}")
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


parser = argparse.ArgumentParser()
parser.add_argument("operation", help="Operation to perform: 'init' initializes necessary files and directories")

args = parser.parse_args

if __name__ == "__main__":
    args = parser.parse_args()
    if args.operation.lower() == 'init':
        # upfront or docker-compose commands fail.
        check_and_create_service_env('./turbosrc-ingress-router/service.env')
        check_and_create_service_env('./turbosrc-egress-router/service.env')

        MODE = initialize_files()
        update_api_token()
        manage_docker_service('start')
        manage_docker_service('stop')
        validate_and_update_endpoint_url()
        update_turbosrc_id_egress_router_url_in_env_file('./turbosrc-ingress-router/service.env')
        update_turbosrc_id_egress_router_url_in_env_file('./turbosrc-egress-router/service.env')
        if MODE != 'router-client':
            remove_egressURLoption()
        if MODE == 'router-client':
            update_egressURLoption()
            update_turbosrc_id_egress_router_url_in_env_file('./turbosrc-ingress-router/service.env')
            update_chrome_extension_config()
        if MODE == 'router-host':
            update_turbosrc_url("http://turbosrc-egress-router:4006/graphql")
            update_chrome_extension_config()

    else:
        usage()
