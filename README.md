<p align="leftr">
  <a href="https://turbosrc.org#gh-light-mode-only">
    <img src="images/turbosrc-light-big.png" width="500px" alt="TurboSrc logo"/>
  </a>
  <a href="https://turbosrc.org#gh-dark-mode-only">
    <img src="images/turbosrc-dark-big.png" width="500px" alt="TurboSrc logo"/>
  </a>
</p>

Turbosrc allows maintainers to create vote power on pull requests on their projects. Now their open source communities can be fully-engaged and participate in the project in a more transparent way.

Turbosrc is under rapid development and in pre-launch phase.

# About

**VotePower**

VotePower grants you a single vote on a pull request, allowing you to vote either for merges or against them to close. You can possess more than one VotePower (e.g., 100,000 VotePower). The total supply of VotePowers is capped at one million per project. Thus, if you hold 100,000 VotePower, you have 100,000 votes at your disposal.

**Use**

If you hold VotePower for a project, simply visit its pull request page on Github. Features will load that allow you to vote and monitor ongoing activities. If you wish to add your project to Turbosrc, navigate to your project's Github page and open the Extension. The Extension will provide an option to add your project to Turbosrc. It will prompt you to sign into your Github account for authentication.

**Get VotePower**

Join the community of the project in which you seek VotePower. Project maintainers are advised to distribute VotePower to their contributors based on merit or to their sponsors.

**More on VotePower**

The supply of VotePower is created by the initial maintainer for each project independently. You could possess 1 VotePower on Project A, 500,000 VotePower on Project B, or none at all on Project C, and so on.

# Step 1: Install

### Make Turbosrc Directory

```
mkdir turbosrc
```

### Clone each service into turbosrc directory
```
git clone git@github.com:turbo-src/turbosrc-service.git
```
```
git clone git@github.com:turbo-src/turbosrc-engine.git
```
```
git clone git@github.com:turbo-src/turbosrc-namespace.git
```
```
git clone git@github.com:turbo-src/turbosrc-gh.git
```
```
git clone git@github.com:turbo-src/turbosrc-chrome-extension.git
```

# Step 2: Configure Turbosrc-service
Complete the instructions for the turbosrc-servcice installation found <a href="https://github.com/turbo-src/turbosrc-service#custom-variables" target="_blank">here</a> and return to these instructions when ready to start.

### Start Services
Ensure Docker is running and from the ```turbosrc/turbosrc-service``` directory:
```
./tsrc-dev start
```

# Step 3: Load the extension
From the ```turbosrc/chrome-extension``` directory:
```
yarn install
```
```
yarn devLocal
```
### Then:
In a Chromium based web browser:
- Go to Manage Extensions
- Enable developer mode
- Select Load unpacked
- Select the ```dist``` directory in ```turbosrc/chrome-extension```. You can then open the Turbosrc web extension in your browser.

![loadextension](https://github.com/turbo-src/turbo-src/assets/75996017/ca652882-92ee-4dbd-9c55-781e8c63613a)

## See here for more detailed instructions to install each service

* [Turbosrc web extension](https://github.com/turbo-src/extension/tree/alpha-devOps)
* [Turbosrc main service](https://github.com/turbo-src/turbosrc-service/tree/alpha-devOps)
* [Turbosrc engine](https://github.com/turbo-src/turbosrc-reibase-engine/tree/alpha-devOps)
* [Turbosrc namespace](https://github.com/turbo-src/turbosrc-reibase-namespace/tree/alpha-devOps)
* [Turbosrc gh](https://github.com/turbo-src/turbosrc-reibase-gh/tree/alpha-devOps)

## Further install instructions (development)

These are for test automation and other devops uses.

### jwt_hash_decrypt

Follow the instructions at `https://github.com/turbo-src/jwt_hash_decrypt`

### fork-repo tool

Follow instructions `github.com/turbo-src/fork-repo`.

### create_pull_requests tool

Follow instructions `github.com/turbo-src/create_pull_requests`

### GihtubMakerTools

Follow instructions `github.com/turbo-src/GihtubMakerTools`.

# Forall Command:
### Create forall command
In the ```turbosrc``` directory:
```
touch forall
```

### And paste in:
```
#!/bin/bash
# https://stackoverflow.com/questions/51544446/can-i-use-git-bash-to-checkout-a-particular-branch-on-all-my-repos-at-once

# ./forall git fetch upstream
# ./forall git checkout relase9.5


for repo in */ ; do
    (   cd "$repo"
        "$@"
    )
done
```
### Then:
```
chmod +x forall
```
