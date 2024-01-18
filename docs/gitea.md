# Gitea

docker-compose build gitea

docker-compose up -d gitea

### How to create a pull request programmatically

docker-compose exec -it gitea bash

cd /data/git/repositories/<repo>

git config --global --add safe.directory /data/git/repositories/<user>/<repo>.git

su - git

cd /data/git/repositories/<user>/<repo>

git remote add <location> <url>

git fetch --all

git update-ref refs/heads/<branch> refs/remotes/<location>/<branch>


### Idea on creating repo on gitea

```
import subprocess

def clone_and_push(github_repo, branch, gitea_repo):
    local_dir = "temp_repo"

    # Clone the branch from GitHub
    subprocess.run(["git", "clone", "-b", branch, "--single-branch", github_repo, local_dir], check=True)

    # Change directory to the cloned repo
    subprocess.run(["cd", local_dir], check=True)

    # Add Gitea repo as a remote
    subprocess.run(["git", "remote", "add", "gitea", gitea_repo], check=True)

    # Push the branch to Gitea
    subprocess.run(["git", "push", "gitea", branch], check=True)

# Example usage
github_repo_url = "https://github.com/user/repo.git"
branch_name = "feature-branch"
gitea_repo_url = "https://gitea.yourdomain.com/user/repo.git"

clone_and_push(github_repo_url, branch_name, gitea_repo_url)
```