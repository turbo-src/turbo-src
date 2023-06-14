<p align="leftr">
  <a href="https://turbosrc.org#gh-light-mode-only">
    <img src="images/turbosrc-light-big.png" width="500px" alt="TurboSrc logo"/>
  </a>
  <a href="https://turbosrc.org#gh-dark-mode-only">
    <img src="images/turbosrc-dark-big.png" width="500px" alt="TurboSrc logo"/>
  </a>
</p>

***Empower Your Open Source Community***

Turbosrc is an innovative tool that equips maintainers with the power to create a voting system for pull requests on their projects. Enhance your open source community's engagement and foster transparency by giving your community the ability to voice their opinions.

As of now, Turbosrc is undergoing rapid development and is in its pre-launch phase. We appreciate your support and patience as we work to make Turbosrc a tool for every open source project.

## What is VotePower?
VotePower gives users the ability to vote on pull requests. Each VotePower represents a single vote that you can use to vote for or against pull requests. Even though you can possess more than one VotePower (for instance, 100,000 VotePower), the total supply is capped at one million per project. In other words, if you hold 100,000 VotePower, you have 100,000 votes that you can use.

## How to Use Turbosrc?
Using Turbosrc is simple! If you hold VotePower for a project, visit its pull request page on Github. You'll see features that allow you to vote and monitor ongoing activities.

To add your project to Turbosrc, visit your project's Github page and open the Turbosrc Extension. You'll see an option to add your project to Turbosrc. You'll need to sign in to your Github account to authenticate yourself.

## How to Get VotePower?
You can get VotePower by joining the community of the project you're interested in. We recommend project maintainers to distribute VotePower to their contributors and sponsors based on merit.

Remember, the supply of VotePower is created by the initial maintainer for each project independently. Therefore, your VotePower might vary across different projects.

## Getting Started with Turbosrc
We've compiled a simple guide to get you started with Turbosrc:

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

**jwt_hash_decrypt**
You can follow the instructions at this link.

**fork-repo tool**
You can follow the instructions at this link.

**create_pull_requests tool**
You can follow the instructions at this link.

**GithubMakerTools**
You can follow the instructions at this link.

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
