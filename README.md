<p align="leftr">
  <a href="https://turbosrc.org#gh-light-mode-only">
    <img src="images/turbosrc-light-big.png" width="500px" alt="TurboSrc logo"/>
  </a>
  <a href="https://turbosrc.org#gh-dark-mode-only">
    <img src="images/turbosrc-dark-big.png" width="500px" alt="TurboSrc logo"/>
  </a>
</p>

We at [Reibase](https://reibase.rs) created the open-source protocol Turbosrc.

Turbosrc software will also tokenize itself, creating value for our contributor community. If you're interested in contributing, see the contributor section below. If you'd like to join our team, please reach out to us at Reibase.

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
```
./forall git fetch --all
```
```
./forall git checkout alpha-docs
```

## See here to install each service

* [Turbosrc web extension](https://github.com/turbo-src/extension/tree/alpha-devOps)
* [Turbosrc main service](https://github.com/turbo-src/turbosrc-service/tree/alpha-devOps)
* [Turbosrc engine](https://github.com/turbo-src/turbosrc-reibase-engine/tree/alpha-devOps)
* [Turbosrc namespace](https://github.com/turbo-src/turbosrc-reibase-namespace/tree/alpha-devOps)
* [Turbosrc gh](https://github.com/turbo-src/turbosrc-reibase-gh/tree/alpha-devOps)

## Further install instructions (development)

This for test automation and not used in turbo-src.

### fork-repo tool

Follow instructions `github.com/turbo-src/fork-repo`.

### create_pull_requests tool

Follow instructions `github.com/turbo-src/create_pull_requests`

### GihtubMakerTools

Follow instructions `github.com/turbo-src/GihtubMakerTools`.