import os
import json
import subprocess
import argparse
import requests
import re
import traceback
import sys

def usage():
    print("Usage: script.py [init USERNAME REPO ACTION]")
    print("  init: initialize necessary files and directories")
    exit(1)


def initialize_files():
    with open('./turbosrc.config', 'r') as f:
        lines = f.readlines()
    USER = lines[0].strip()
    GITHUB_API_TOKEN = lines[1].strip()
    SECRET = lines[2].strip()
    ADDR = lines[3].strip() if len(lines) > 3 and is_valid_eth_address(lines[3].strip()) else None

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
        lines = f.readlines()
    secret = lines[2].strip()

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
    try:
        with open('./turbosrc-service/.config.json', 'r') as f:
            data = json.load(f)

        url = data['namespace']['endpoint']['url']
        token = data['github']['apiToken']
        contributor_name = data['github']['user']

        query = f"""
        {{
            findOrCreateUser(owner: "", repo: "", contributor_id: "", contributor_name: "{contributor_name}", contributor_signature: "", token: "{token}") {{
                contributor_name,
                contributor_id,
                contributor_signature,
                token
            }}
        }}
        """

        response = requests.post(f"{url}/graphql", json={'query': query}, headers={"accept": "json"})
        response.raise_for_status()
        result = response.json()
        return result['data']['findOrCreateUser']['contributor_id']
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
    subprocess.run(['docker-compose', 'up', '-d', 'namespace-service'], check=True)
    if action == 'stop':
        subprocess.run(['docker-compose', 'down', '-v', 'namespace-service'], check=True)


parser = argparse.ArgumentParser()
parser.add_argument("operation", help="Operation to perform: 'init' initializes necessary files and directories")

args = parser.parse_args

if __name__ == "__main__":
    args = parser.parse_args()
    if args.operation.lower() == 'init':
        initialize_files()
        update_api_token()
        manage_docker_service('start')
        contributor_id = get_contributor_id()

        if contributor_id is not None:
            update_contributor_id(contributor_id)
        else:
            print("Failed to fetch contributor id. Exiting...")
            sys.exit(1)

        manage_docker_service('stop')
    else:
        usage()
