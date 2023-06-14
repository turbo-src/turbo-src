<p align="leftr">
  <a href="https://turbosrc.org#gh-light-mode-only">
    <img src="images/turbosrc-light-big.png" width="500px" alt="TurboSrc logo"/>
  </a>
  <a href="https://turbosrc.org#gh-dark-mode-only">
    <img src="images/turbosrc-dark-big.png" width="500px" alt="TurboSrc logo"/>
  </a>
</p>

## Launch Your Own Turbosrc Instance
Turbosrc amplifies community involvement and fosters transparency in your open-source projects by setting up a unique voting system for your projects' pull requests. Though we're currently in the pre-launch phase and actively developing, we appreciate your support and patience and strive to make Turbosrc a useful tool for all open-source projects.

## Understanding VotePower
VotePower gives users in your Turbosrc instance the ability to vote on pull requests. Each VotePower represents a single vote that they can use to vote for or against pull requests. Although a user can possess more than one VotePower (for instance, 100,000 VotePower), the total supply is capped at one million per project within your Turbosrc instance. In other words, if a user holds 100,000 VotePower, they have 100,000 votes that they can use.

Remember, VotePower is specific to each project. This means if you possess VotePower in one project, it cannot be used in another.

## How to Distribute VotePower?
You can distribute VotePower to the community members of the project you're hosting on your Turbosrc instance. On your Github page you added to Turbosrc, you can look up a users via the web extension. From there you you can transfer VotePower. The users have to sign up (a few clicks only) using the web extension.

We recommend project maintainers to distribute VotePower to their contributors and sponsors based on merit.

Remember, the supply of VotePower is created by the initial maintainer for each project independently within your Turbosrc instance. Therefore, the distribution of VotePower might vary across different projects.

## How to Use Turbosrc?
Setting up and using Turbosrc is simple! If users hold VotePower for a project within your Turbosrc instance, they can visit its pull request page on Github and see features that allow them to vote and monitor ongoing activities.

To add your project to your Turbosrc instance, visit your project's Github page and open the Turbosrc Extension. You'll see an option to add your project to Turbosrc. You'll need to sign in to your Github account to authenticate yourself.

## Setting up a Turbosrc Instance
We've compiled a simple guide forthose that want to manage a Turbosrc instance:

### Step 1: Installation
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

### Step 2: Configure Turbosrc Service
Before you can use Turbosrc, you'll need to configure it. Follow the instructions for the Turbosrc service installation <a href="https://github.com/turbo-src/turbosrc-service#custom-variables" target="_blank">here</a> and then return to this README to continue.

### Step 3: Launch Turbosrc
Make sure Docker is running and then start services from the Turbosrc service directory
```
cd turbosrc-service
./tsrc-dev start
```

### Step 3: Load the Extension
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
