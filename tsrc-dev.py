import os
import json
import subprocess
import argparse

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
    ADDR = lines[3].strip()

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

parser = argparse.ArgumentParser()
parser.add_argument("operation", help="Operation to perform: 'init' initializes necessary files and directories")

args = parser.parse_args

if __name__ == "__main__":
    args = parser.parse_args()
    if args.operation.lower() == 'init':
        initialize_files()
        update_api_token()
    else:
        usage()