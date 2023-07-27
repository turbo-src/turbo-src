## Launch turbosrc with routing

1. Go to AWS > EC2 > N. California

2. Launch turbosrc-ngnix and turbosrc from EC2 dashboard

3. Select the turbosrc-ngnix > Connect (console)

3. Select the turbosrc > Connect (console)

### turbosrc-ngnix

Start nginx.

```
sudo systemctl start nginx
```

View nginx config.

```
vim /etc/nginx/nginx.conf
```

Edit nginx config.

```
vim /etc/nginx/nginx.conf
```

Validate nginx config.

```
sudo nginx -t
```

Reload nginx config.

```
sudo nginx -s reload
```