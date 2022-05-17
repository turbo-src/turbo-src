# turbo-src

Requirements

* Docker installed.
* git installed

## Setup Mac

macOS Catlina (10.15) (or higher)


### Install brew and upgrade

Brew is a package manager for Mac. You can check if you already have it with:

`whereis brew`


If not there, install (check if below command is correct, here https://brew.sh/).

/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)”

`brew update && brew upgrade`

### Install developer tools.

`xcode-select --install`

## Install Docker

For Mac.

Search the web for "Docker install Mac".

Otherwise install Docker from a package manager or however.

Make sure to be able to run docker commands without root, otherwise development and test scripts won't work.

```
sudo groupadd docker
sudo usermod -aG docker [user]
```


Test that it works. You don't need to be in any particular directory.

`docker run hello-world`


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

## Install yarn

Yarn is an alternative package manager for nodejs

Download the public key from yarn author.

`curl -sL https://dl.yarnpkg.com/debian/pubkey.gpg | sudo apt-key add -`

Add the public key so ubuntu package manager can find it.

`echo "deb https://dl.yarnpkg.com/debian/ stable main" |
sudo tee /etc/apt/sources.list.d/yarn.list`

Finally, install.

`sudo apt update && sudo apt install yarn`

## Install git, if not already there.

Git is a version control system. Check if you already have it.

`whereis git`

If not, install it.

### Mac

`brew install git`

### Configure git.

Suggest that you use your github username.

```
git config --global user.name "YOUR_USERNAME_HERE"
git config --global user.email ""
git config -l
```
### Github

Invite the user to turbo-src organization on Github.

github.com/turbo-src > Invite Someone (right side of page)

## Install GithubMakerTools

See [here](https://github.com/turbo-src/GithubMakerTools).

## service install

Clone the repo.

`git clone https://github.com/turbo-src/service turbosrc-service`

`cd turbsrc-service`

Install everything.

`npm install`

If install doesn't work, make sure your using nodejs 12.22.0

`node --version`

## extension install

Clone the repo.

```
git clone https://github.com/turbo-src/extension turbosrc-extension`
```

Install.

```
yarn install
```

See it's readme under `Development` section.

https://github.com/turbo-src/extension

## Workflow

### service

Rebuilds image, starts containers, and runs tests.

```
./testing/run-tests.sh
```

### extension

Output the files for extension

```
yarn dev
```

May want to interupt file watching after it emits file as it's very cpu intensive.

Go to you chrome or brave browser

Open

brave://extensions/

or

chrome://extensions/

Select Load Unpacked and select the `dist` folder in the `turbosrc-extension`.

## Notes


### Alternative install of nodejs using nvim.

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
