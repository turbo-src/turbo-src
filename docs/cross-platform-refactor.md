
## Testing capabilities

- [ ] programmatically create and destroy gitea instance
- [ ] git test-repo with branches
- [ ] gitea admin create user
- [ ] gitea admin create public key on behalf of user
- [ ] gita admin create repo - test-repo
- [ ] push test-repo branches to gitea
- [ ] tests cases using gitea remote and api key
- [ x ] clone repo
- [ x ] fetch and pull branch
- [ x ] switch branches
- [ x ] push branch
- [ x ] check mergeable
- [ x ] check rebasible

## Other

1. Client provides remoteURL of pull request branch.

2. Client provides head of pull request branch.

3. Call `fetchAndPullBranch.js(repoID, branchName, forkRemoteURL)`

    repoID is calculated as follows:

    `crypto.SHA256(remoteURL).toString(crypto.enc.Hex)`

    branchName should be ${defaultHash/forkRemoteURL} to prevent clashes.

4. Verify branch head with `getBranchHead`.

5. Push branch to remoteURL

   `pushBranch(repoID, remoteURL, branch)

6. `createTurboSrcPullRequest` calls gitea api to create/close/merge pr

7. Delete branch after the pull request is closed or is merged