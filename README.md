<p align="leftr">
  <a href="https://turbosrc.org#gh-light-mode-only">
    <img src="images/turbosrc-light-big.png" width="500px" alt="TurboSrc logo"/>
  </a>
  <a href="https://turbosrc.org#gh-dark-mode-only">
    <img src="images/turbosrc-dark-big.png" width="500px" alt="TurboSrc logo"/>
  </a>
</p>

Turbosrc allows maintainers to create vote power on pull requests on their projects. Now their open source communities can be fully-engaged and participate in the project in a more transparent way.

Turbosrc is under rapid development and is in alpha phase

# Install

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

### Create forall command
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

### To start using locally:
Complete the instructions for the turbosrc-servcice installation found <a href="https://github.com/turbo-src/turbosrc-service#custom-variables" target="_blank">here</a> and return here when complete.

### Start the services:
From ```turbosrc/turbosrc-service```
```
./tsrc-dev start
```
### Then:
from the ```turbosrc/chrome-extension``` directory:
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
