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

    if ADDR:
        if not is_valid_ethereum_address(ADDR):
            ADDR = None
    else:
        ADDR = None

    if None in (USER, GITHUB_API_TOKEN, SECRET):
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
               "url": "http://turbosrc-service:4000/graphql"
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

def update_api_token():
    with open('./turbosrc-service/.config.json', 'r') as f:
        data = json.load(f)

    apiToken = data['github']['apiToken']

    with open('./turbosrc.config', 'r') as f:
        data = json.load(f)

    secret = data.get('SECRET')

    decryptedToken = subprocess.check_output([
        'docker-compose', 'run', '--rm', 'jwt_hash_decrypt', '--secret=' + secret, '--string={\"githubToken\": \"' + apiToken + '\"}'
    ]).decode('utf-8').split('\n')[-2]

    data['github']['apiToken'] = decryptedToken

    with open('./turbosrc-service/.config.json', 'w') as f:
        json.dump(data, f, indent=4)

def is_valid_ethereum_address(address):
    try:
        return bool(re.match("^0x[a-fA-F0-9]{40}$", address))
    except Exception as e:
        print(f"Failed to check if provided string is a valid Ethereum address. Error: {str(e)}")
        traceback.print_exc()
        return False

def get_contributor_id():
    last_exception = None
    try:
        with open('./turbosrc-service/.config.json', 'r') as f:
            data = json.load(f)

        url = 'http://localhost:4003'  # data['namespace']['endpoint']['url']
        token = data['github']['apiToken']
        contributor_name = data['github']['user']

        query = f"""
        {{
            findOrCreateUser(owner: "", repo: "", contributor_id: "none", contributor_name: "{contributor_name}", contributor_signature: "none", token: "{token}") {{
                contributor_name,
                contributor_id,
                contributor_signature,
                token
            }}
        }}
        """

        max_retries = 5  # Number of attempts before printing an error message

        for i in range(max_retries):
            try:
                response = requests.post(f"{url}/graphql", json={'query': query}, headers={"Content-Type": "application/json", "Accept": "application/json"})
                response.raise_for_status()
                result = response.json()
                if result.get('data') and result['data'].get('findOrCreateUser'):
                    return result['data']['findOrCreateUser']['contributor_id']
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
        print(f"Failed to get contributor id. Error: {str(e)}")
        traceback.print_exc()
        return None

def update_contributor_id(contributor_id):
    try:
        with open('./turbosrc-service/.config.json', 'r') as f:
            data = json.load(f)

        current_address = data['turbosrc']['store']['contributor']['addr']

        if not is_valid_ethereum_address(current_address):
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
                # Try to fetch contributor id
                contributor_id = get_contributor_id()
                # If fetch is successful, update contributor_id and break from loop
                if contributor_id is not None:
                    update_contributor_id(contributor_id)
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

parser = argparse.ArgumentParser()
parser.add_argument("operation", help="Operation to perform: 'init' initializes necessary files and directories")

args = parser.parse_args

if __name__ == "__main__":
    args = parser.parse_args()
    if args.operation.lower() == 'init':
        initialize_files()
        update_api_token()
        manage_docker_service('start')
        manage_docker_service('stop')
    else:
        usage()
