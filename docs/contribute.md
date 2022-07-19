# Contribute

### Nix demo

We want to run a demo off of nixos/nixpkgs.

1. Fork the project
2. Checkout commit down from HEAD~10
3. Make a branch from each commit HEAD to HEAD~10

(test script push --all origin)

nixpkgs is modular, so most commits don't touch the same files. No merge conflicts that can't be automatically resolved in general. Feel free to skip a commit if there is a confict (as long makes sense visually).

Put the nixpkgs in turbo-src/nixpkgs. Should be forked at the commit depth you want. Whatever you need to do to get it done.

### ~~Signup page~~

~~Allow people to follow the project by adding their email.~~

### ~~Github repo create and del~~

~~Programmatically create and delete a Github repo.~~

* ~~Puppeter?~~
* ~~Github Api?~~

### Github pull page diffs

Programmatically diff the DOM to detect any breaking changes to Github website.

* Existing tools?

### Fake Github API service for testing.

Server that responds like the Github API for testing purposes.

### Resource consumption regression tests

Benchmark memory usage, cpu, and network of turbo-src service and extension. Should be able to assert certain acceptable ranges in tests.

### Token wallet

Demonstrate gettting Metamask or Avalanch wallet to popup by injecting wallet api into a webpage.

### Popup vote table

Stablize the vote table feature. Currently it uses a websocket, but messages are missed. Perhaps go simple with polling for now.

### Token wallet

Demonstrate gettting Metamask or Avalanch wallet to popup by injecting wallet api into a webpage.

### Wormhole

Setup a private wormhole server.

### Docker to podman and buildah

Build the service image using buildah and run with podman. Document for switch.
