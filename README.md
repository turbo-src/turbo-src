# turbo-src
## Setup Mac

macOS Catlina (10.15) (or higher)

### Install Brew (Mac only)

`xcode-select --install`
Brew is a package manager for Mac.

Check if you have it.

`whereis brew`

If not there, install (check if below command is correct, here https://brew.sh/).

/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)”

## Setup Linux (Ubuntu)

Docker installed.
git installed

### Install Brew (Mac only)

`xcode-select --install`
Brew is a package manager for Mac.

Check if you have it.

`whereis brew`

If not there, install (check if below command is correct, here https://brew.sh/).

/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)”

### Stuff to do before

On Linux

`sudo apt update`

On Mac.
w
`brew update && brew upgrade`

whereis brew

`mkdir ~/turbo-src`

`cd ~/turbo-src`

### Setup yooo

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