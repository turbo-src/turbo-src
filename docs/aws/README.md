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

## Security Rules

### turbosrc-nginx

Here are the following rules for the security group on AWS:

Inbound rules

```
| Name | Security Group Rule ID | IP Version | Type  | Protocol | Port Range | Source         | Description                  |
|------|------------------------|------------|-------|----------|------------|----------------|------------------------------|
| –    | placeholder-id-1       | IPv4       | SSH   | TCP      | 22         | 13.52.6.112/29 | EC2 Instance Connect only    |
| –    | placeholder-id-2       | IPv4       | HTTPS | TCP      | 443        | –              | –                            |

```

Outbound rules

```
| Name | Security Group Rule ID | IP Version | Type       | Protocol | Port Range | Destination | Description |
|------|------------------------|------------|------------|----------|------------|-------------|-------------|
| –    | placeholder-id-1       | IPv4       | All traffic| All      | All        | –           | –           |
```

In order to ascertain AWS ip range for `source` in the inbound SSH rule, I used the following script.

```
import requests

def get_ec2_instance_connect_ip_ranges(region):
    # URL for the AWS IP ranges JSON
    AWS_IP_RANGES_URL = "https://ip-ranges.amazonaws.com/ip-ranges.json"

    # Fetch the JSON data
    response = requests.get(AWS_IP_RANGES_URL)
    data = response.json()

    # Extract relevant IP ranges
    ip_ranges = [
        prefix['ip_prefix'] for prefix in data['prefixes']
        if prefix['service'] == 'EC2_INSTANCE_CONNECT' and prefix['region'] == region
    ]

    return ip_ranges

if __name__ == "__main__":
    region = "us-west-1"  # Northern California
    ip_ranges = get_ec2_instance_connect_ip_ranges(region)

    print(f"EC2_INSTANCE_CONNECT IP ranges for {region}:")
    print(ip_ranges)
```
