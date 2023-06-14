<p align="left">
  <a href="https://turbosrc.org#gh-light-mode-only">
    <img src="images/turbosrc-light-big.png" width="500px" alt="TurboSrc logo"/>
  </a>
  <a href="https://turbosrc.org#gh-dark-mode-only">
    <img src="images/turbosrc-dark-big.png" width="500px" alt="TurboSrc logo"/>
  </a>
</p>
<p align="left">
  <em><strong>Empowering open source communities</em></strong>
</p>

<br>

TurboSrc is a unique platform designed to promote transparency and boost community participation in your open-source projects. Our innovative voting system for pull requests not only empowers contributors but also enriches the overall development experience.

It currently works as a Chrome web extension for Github, but the plan is to develop it across multiple code hosts if necessary. The Turbosrc instance has a full api and its own internal representation of code bases and their pull requests.

While we're currently in active development and the pre-alpha phase, your support and patience are much appreciated. Our goal is to develop TurboSrc into a valuable tool for all open-source projects.

## Highlights
* **Launch Your Own TurboSrc Instance:** Enhance your project's community involvement by setting up your unique TurboSrc instance.
* **Harness VotePower:** Empower your TurboSrc instance users with the ability to vote on pull requests using VotePower.
* **Effortless VotePower Distribution:** Distribute VotePower to your project's community members directly through your Github page integrated with TurboSrc.

Let's get you started!

## Understanding VotePower
In your TurboSrc instance, each user has the capacity to vote on pull requests, courtesy of VotePower. Essentially, each VotePower translates to a single vote that can be cast for or against pull requests. Although a user may possess multiple VotePowers (e.g., 100,000 VotePower), the total supply is capped at one million per project within your TurboSrc instance. So, if a user holds 100,000 VotePower, they have 100,000 votes at their disposal.

Note: VotePower is specific to each project. Consequently, if you hold VotePower in one project, it cannot be used in another.

## Distributing VotePower
As a project maintainer, you can distribute VotePower to the community members of the project hosted on your TurboSrc instance. Simply look up users via the web extension on your Github page linked with TurboSrc, and transfer VotePower to them. Users can sign up conveniently via the web extension.

We encourage project maintainers to distribute VotePower to their contributors and sponsors, recognizing and rewarding their merit.

Bear in mind, the supply of VotePower is created by the initial maintainer for each project independently within your TurboSrc instance. Hence, the distribution of VotePower might differ across various projects.

## TurboSrc Usage
TurboSrc is designed for simplicity and ease of use. Users holding VotePower for a project within your TurboSrc instance can easily visit its pull request page on Github and utilize features that allow them to vote and track ongoing activities.

To add your project to your TurboSrc instance, visit your project's Github page and open the TurboSrc Extension. There you will find an option to add your project to TurboSrc. Just sign in to your Github account for authentication.

## Setting up a TurboSrc Instance
Setting up your own TurboSrc instance is straightforward. Here's a step-by-step guide to help you get started:c instance:

**1. Installation**
To begin, set up the Turbosrc directory and clone each service:

```
# Create Turbosrc directory
mkdir turbosrc

# Navigate to the directory
cd turbosrc

# Clone each service into the directory
git clone git@github.com:turbo-src/turbosrc-service.git
git clone git@github.com:turbo-src/turbosrc-engine.git
git clone git@github.com:turbo-src/turbosrc-namespace.git
git clone git@github.com:turbo-src/turbosrc-gh.git
git clone git@github.com:turbo-src/turbosrc-chrome-extension.git
```
## Setting up a Turbosrc Instance
We've compiled a simple guide forthose that want to manage a Turbosrc instance:

**2. Configure Turbosrc Service**

You'll need a `.config.json` file in the root directory of turbosrc-service.

#### 1. A Github API Token

[See here.](https://docs.github.com/en/enterprise-server@3.4/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)

#### 2. Create YOUR_SECRET

It can be anything, as long as no one can guess it.

#### 3. Create YOUR_ENCRYPTED_TOKEN

To create `YOUR_ENCRYPTED_TOKEN`, install [**jwt_hash_encrypt**](github.com/turbo-src/jwt_hash_decrypt) and run the command below (edit with your info).

```
node jwt_hash_decrypt.js --secret=YOUR_SECRET --string='{"githubToken": "ghp..."}'
```
#### 4. Create `turbosrc-service/.config.json`
   
- Replace YOUR_USERNAME with your Github username
- Replace YOUR_SECRET with your secret to sign the token
- Replace YOUR_ENCRYPTED_TOKEN with the JWT string from **'step 2'** above

```
{
    "github": {
        "organization": "turbo-src",
        "user": "YOUR_USERNAME",
        "apiToken": "YOUR_ENCRYPTED_TOKEN"
    },
    "turbosrc": {
        "endpoint": {
          "mode": "online",
           "url": "http://localhost:4000/graphql"
        },
        "jwt": "YOUR_SECRET",
        "store": {
            "repo": {
                "addr": "REPO_ADDR",
                "key": "REPO_KEY"
            },
            "contributor": {
                "addr": "YOUR_ADDR",
                "key": "YOUR_KEY"
            }
        }
    },
    "offchain": {
        "endpoint": {
          "mode": "online",
          "url": "http://localhost:4002/graphql"
        }
    },
    "namespace": {
        "endpoint": {
          "mode": "online",
          "url": "http://localhost:4003/graphql"
        }
    },
    "gh": {
        "endpoint": {
          "mode": "online",
          "url": "http://localhost:4004/graphql"
        }
    },
    "testers": {}
    }
}
```

Before you can use Turbosrc, you'll need to configure it. Follow the instructions for the Turbosrc service installation <a href="https://github.com/turbo-src/turbosrc-service#config" target="_blank">here</a> and then return to this README to continue.

**3. Launch Turbosrc**
Make sure Docker is running and then start services from the Turbosrc service directory
```
cd turbosrc-service
./tsrc-dev start
```

**4. Load the Extension**
From the chrome-extension directory, install dependencies and start the local development server:
```
# Install dependencies
yarn install

# Start the local development server
yarn devLocal
```

Then, in a Chromium based web browser:

1. Go to Manage Extensions
2. Enable developer mode
3. Select Load unpacked
4. Select the `dist` directory in `turbosrc/chrome-extension`. You can then open the Turbosrc web extension in your browser.

![loadextension](https://github.com/turbo-src/turbo-src/assets/75996017/ca652882-92ee-4dbd-9c55-781e8c63613a)

For more detailed instructions on each service installation, check out the respective links below:

* [Turbosrc web extension](https://github.com/turbo-src/extension/tree/alpha-devOps)
* [Turbosrc main service](https://github.com/turbo-src/turbosrc-service/tree/alpha-devOps)
* [Turbosrc engine](https://github.com/turbo-src/turbosrc-reibase-engine/tree/alpha-devOps)
* [Turbosrc namespace](https://github.com/turbo-src/turbosrc-reibase-namespace/tree/alpha-devOps)
* [Turbosrc gh](https://github.com/turbo-src/turbosrc-reibase-gh/tree/alpha-devOps)

## Advanced Installation Instructions (For Development Purposes)
The following instructions are intended for development, test automation, and DevOps uses:

### jwt_hash_decrypt

You can follow the instructions at this [link](https://github.com/turbo-src/jwt_hash_decrypt).

### fork-repo tool

You can follow the instructions at this [link](github.com/turbo-src/fork-repo).

### create_pull_requests tool

You can follow the instructions at this [link](github.com/turbo-src/create_pull_requests)

### GithubMakerTools

You can follow the instructions at this [link](github.com/turbo-src/GihtubMakerTools).

### Creating the 'forall' Command

This command will help you to perform Git commands across all repositories simultaneously.

In the turbosrc directory:

```
# Create the forall script
echo '#!/bin/bash
for repo in */ ; do
    (   cd "$repo"
        "$@"
    )
done' > forall

# Make the script executable
chmod +x forall
```

You can then use this script to run Git commands on all repositories at once. For example:
```
# Fetch from upstream for all repositories
./forall git fetch upstream

# Switch to the release 9.5 branch for all repositories
./forall git checkout release9.5
```
