# Contributions Needed

### Signup page

Allow people to follow the project by adding their email.

### Github repo create and del

Programmatically create and delete a Github repo.

* Puppeter?
* Github Api?

### Github pull page diffs

Programmatically diff the DOM to detect any breaking changes to Github website.

* Existing tools?

### Fake Github API service for testing.

Server that responds to like Github API for testing purposes.

### Resource consumption regression tests

Benchmark memory usage, cpu, and network of turbo-src service and extension. Should be able to assert certain acceptable ranges in tests.

### SVG icons

Properly convert image icons to svg in the extension codebase.

### Git server

Hosts the repo. All pull request forks are validated here. Also the `turbo-src pull request id` (sha256 of repo) is generated here.

Node.js entry point with a queue.

General gist using git cli as an example.

Add the pull requester to remote.

`git remote add  $user https://github.com/$user/$repo`

Get the branch.

`git pull $user $branch`

`git checkout $branch`

Calculate sha256 `tprid`.

turbo-src service will map the `tprid` to the `issue_id` on Github.

Rename branch by the `tprid`.

```
git checkout -b $tprid && \
git branch -D $branch
```

Validate a voted and merged in pull request. Make sure the `tPRID` hasn't changed.

```
git pull $user $branch
```
Once merged, validate Github master.

```
git pull github master
```
Calculate sha256 `tprid`.

If `tprid` matches contract `head`, then valid. A message in the popup will say the repo is valid. If invalid, vote buttons will say ('invalid`), and modal will explain why.
