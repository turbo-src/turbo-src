# Authenication

Let's deal with the reality. Pub and priv key authentication is supreme for authenticating clients. It enables trust in that clients are guaranteed that no one can authenticate, not even the server. It also enables shared secrets, allowing for secure communciations channels.

However, you can't expect users, to hold private keys. They may use the application rarely and may forget about the keys. Also they aren't professional coders and can't be expected to store private keys at the threat of losing access to their accounts.

## Instance

Currently authenticates using public and private keys. Not even the instances can fake a user action. They could, but any audit would show they lied.

## User

They must be able to login with a username and password. And they must be able to reset there username and password using a trusted third-party of their choice, such as Google, Github, Facebook, etc.

There has to be room left to allow some users that want to to authenticate using cryptography, as an instance. So the reasonable thing is if a user wants that level of security and responsibility, they must be an instance owner

### Default user

Here's an idea:

```
trsc user create -username [username] -password [password] --auth <github/...> --tsrcid [tsrcid]
```

This output includes a link they can click on to authenticate.

The user can also reset their password by running.

```
tsrc user reset -username -newpassword -oldpasword
```

#### create-user

git-service/giteaCreateUserWithPassword is called. A gitea user is created with the same username and password.

It then calls git-service/giteaTokenCreator. A access token is created.

service populates createUser(..., token) with it.

Whenever service calls git-service or other services for user, it must pass the token.

The user when using the cli app must sign in with a username and password. That username and password must much what's on the git-service.

```userLogin``` when triggerd by a user login, it checks the user exists on gitea under that username and password  by creating an access token. Success means verified. Not, wrong username or password.

It then returns the token to the cli-client, which the cli-client saves in the turbosrc.config on token field. Therefore, the access token is updated and the old deleted on the instance on cli-client (turbosrc.config) on each login.

Whenever the client does any other actions, it must pass the token along with it. The service can simply verifiy the token against the git-service.

**account recovery**

When a user creates an account, they must login with a third-party via Oath2, such as Github. That way they can recover there account with it.

The user should be able to update there third-party authorizer simply with their username and password. If they forget they password and they lose access to the third-party of record, there is no way for them to recover the account.

```
tsrc user reset -username -newpassword -oldpasword -auth [github|...]
```


**password attempts and length**

Best practice is implemented here. I think sudo rules are good. Ten minutes after 3 failed attempts.

**bots protection**

No captchas or bot detection as turbosrc welcomes users deploying bots.

### Instance user

The user passes there public key and signed message along with an actions. Like the router, the instance checks the signed message.