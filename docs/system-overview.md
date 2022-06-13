# System overview

### Authentication

The service will accept any repo_id, which  is

`owner/repo`

The user loads there username and github credentials with .config.json.o

The user must be an accepted user (createUser), and be added to the database via transferTokens or from original createRepo.

The extension checks the owner/repo name from github. If it doesn't match that of the service, it won't work.
