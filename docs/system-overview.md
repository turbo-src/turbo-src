# System overview

## Repos

### repoID

Each repo must have a unique repoID. A repoID is an Ethereum address, whether the repo is 'hosted' on onchain or offchain.


#### Offchain

In order to make it seamless for a user to create several repos without having to create new accounts, the service will generate a unique repoID for them.

### repoName

The repo name can be any name, so long as it's unique to the network host. In order to make it easy for users to own several repos, the repoName is `<owner>/<subRepoName>`. So for example, `reibase/turbosrc` would be a valid repoName. Where reibase is the owner and turbosrc is the name. There would have to be an account named reibase.

### Authentication

The service will accept any repo_id, which  is

`owner/repo`

The user loads there username and github credentials with .config.json.o

The user must be an accepted user (createUser), and be added to the database via transferTokens or from original createRepo.

The extension checks the owner/repo name from github. If it doesn't match that of the service, it won't work.
