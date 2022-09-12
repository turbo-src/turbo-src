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

## Actions

### setVote

* main `service` checks the `namespace` service if the user exists.
* It finds out if there is tPR open. If not it opens and applies the vote.

Must add:
* Check if PR on Github exists (cache `$prID: boolean`)
* Check if PR is mergeable. (cache `mergeable: 0 yes | 1 no | 2 any other, such as null

```
repoCache = {
   $repoID: {
       $prID: boolean
       mergeable: int
   }

}
```

It doesn't need to be written to disk. If the service restarts, it's not expensive to get all this info again. It will automatically happen when users vote on pull requests.
