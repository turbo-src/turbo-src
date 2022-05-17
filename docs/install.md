# turbo-src

Requirements

* Docker installed.
* git installed

## Setup Mac

macOS Catlina (10.15) (or higher)

`mkdir ~/turbo-src/`

`cd ~/turbo-src/`

### Install developer tools.

`xcode-select --install`

### Install Docker

Search the web for "Docker install Mac".

Test that it works. You don't need to be in any particular directory.

`docker run hello-world`

### Install wormhole

See instructions at

github.com/7db9a/magic-wormhole-container

### Install brew and upgrade

Brew is a package manager for Mac. You can check if you already have it with:

`whereis brew`


If not there, install (check if below command is correct, here https://brew.sh/).

/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)”

`brew update && brew upgrade`

## Install nvm (nodejs version manager)

### Mac

Before running

`brew install nvm`

There is some additional setup found here:

https://formulae.brew.sh/formula/nvm

Install node.

`nvm install 12.22.0`

Make sure using the right one

`nvm use 12.22.0`

### Arch

```
pacman -S nvm
```

Then follow these steps:

https://aur.archlinux.org/packages/nvm

### Install git, if not already there.

Git is a version control system. Check if you already have it.

`whereis git`

If not, install it.

`brew install git`

Configure git. Suggest that you use your github username.

```
git config --global user.name "YOUR_USERNAME_HERE"
git config --global user.email ""
git config -l
```
### Github

Invite the user to turbo-src organization on Github.

github.com/turbo-src > Invite Someone (right side of page)

### Remaining setup

`mkidr ~/turbo-src`

`cd ~/turbo-src`

Clone the repo.

`git clone https://github.com/turbo-src/graphql_express_server`

`cd ~/graphql_express_server`

Install everything.

`npm install`

If install doesn't work, make sure your using nodejs 12.22.0

`node --version`

If it isn't correct, make sure you selected right one on nvm.

Transfer `.github-token` file using wormhole. The receiver needs to be in the right directory.

`cd ~/turbo-src/graphql_express_server`

## Linux setup

### Clone the repo

git clone https://github.com/turbo-src/graphql_express_server

## Setup Linux

On Linux

`sudo apt update`

On Mac.

whereis brew

`mkdir ~/turbo-src`

`cd ~/turbo-src`

### Install nodejs using nvim.

Nodejs server-side javascript. This will also install npm, the package nodejs package manager.

Nvim let’s you install and manage different version of nodejs

`curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.38.0/install.sh | bash`

Update paths in bash.

`source ~/.bashrc`

See what versions of node you’re running.

`nvm list-remote`

If you don’t see 12.22.0, install like so.

`nvm install v12.22.0`

Use correct version.

`nvm use v12.22.0`

### Install yarn

Yarn is an alternative package manager for nodejs

Download the public key from yarn author.

`curl -sL https://dl.yarnpkg.com/debian/pubkey.gpg | sudo apt-key add -`

Add the public key so ubuntu package manager can find it.

`echo "deb https://dl.yarnpkg.com/debian/ stable main" |
sudo tee /etc/apt/sources.list.d/yarn.list`

Finally, install.

`sudo apt update && sudo apt install yarn`

### Install turbo-src local server.

Make sure you’re in `~/turbo-src/`. If not sure do `pwd`.

Clone the repo.

`git clone https://github.com/turbo-src/graphql_express_server`

Build the server.

`$ ./dev.sh cycle`

`$ ./dev.sh start`
