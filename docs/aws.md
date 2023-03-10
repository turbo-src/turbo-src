udo yum update -y

## Install git

sudo yum install git -y

## Install docker


It also has instruction on allowing the use of docker without sudo.

Go to section Installing Docker on Amazon Linux 2
https://docs.aws.amazon.com/AmazonECS/latest/developerguide/create-container-image.html

We didn't choose to start docker on startup.

But here it says to do something else, which is different than above

https://gist.github.com/npearce/6f3c7826c7499587f00957fee62f8ee9

Make sure to exit terminal session then rejoin. Otherwise changes for 'no sudo' don't go into effect.

## Docker-compose install

Make sure to do the line that has the current version of docker-compose. otherwise you'll get very old one.

https://gist.github.com/npearce/6f3c7826c7499587f00957fee62f8ee9


## Updating Security Rules

Instances>Select Instance>Security>Security groups (blue link launch-wizard-1)>Edit nbound rules>Add rule

Type: All traffick
Source: Anywhere (ipv4)

Create the rule


## Domain routing

### Get elastic IP address

To determine the IP address of your EC2 instance, you can follow these steps:

Go to the AWS Management Console and navigate to the EC2 dashboard.
In the left-hand menu, click on "Instances" to view a list of your instances.
Select the instance you want to use and look for the "IPv4 Public IP" value in the instance details section.
Alternatively, you can use the Elastic IP feature in AWS to assign a static public IP address to your EC2 instance. This can be helpful if you need to maintain a fixed IP address for your instance, even if you stop and start it. To use Elastic IP, you can follow these steps:

Go to the AWS Management Console and navigate to the EC2 dashboard.
In the left-hand menu, click on "Elastic IPs" to view your available IPs.
Click on the "Allocate new address" button to create a new Elastic IP address.
Select the Elastic IP you just created and click on the "Actions" button.
Click on "Associate IP address" and select the instance you want to associate the IP address with.
Confirm the association and the Elastic IP will be assigned to your instance.
Once you have the IP address of your EC2 instance, you can use it to configure your domain DNS settings to allow incoming traffic to your instance.

## Namecheap

#### Warning setup with subdomain off the bat

To allow incoming traffic from your domain address to your EC2 instance, you need to follow these steps:

Log in to your Namecheap account.
Navigate to the "Domain List" section and select the domain you want to use.
Click on the "Manage" button next to the domain name.
Scroll down to the "Advanced DNS" section and click on the "Add New Record" button.
In the "Type" field, select "A Record" from the dropdown menu.
In the "Host" field, enter the subdomain or leave it blank to use the root domain (e.g., "@" for the root domain).
In the "Value" field, enter the IP address of your EC2 instance.
Leave the "TTL" field as default or change it to your preference.
Click on the "Save All Changes" button to save the new record.
After saving the new A record, it may take some time (up to 24 hours) for the DNS changes to propagate globally. Once the propagation is complete, you can access your EC2 instance using your domain name.

To be clear, if youd don't want a subdomain type '@' without quotes into Host.


## SSL Certificate

### Generate CSR (Certificate Signing Request)

On the Amazon nginx instance

- Organization name is optional so just put ""
- Email is optional but just put it (use the same to be safe as is used to register domain with domain host)
- Challenge password (do it)

The command to generate has a extraneous quote symbol appended to command - remove it
https://www.namecheap.com/support/knowledgebase/article.aspx/9446/2290/generating-csr-on-apache-opensslmodsslnginx-heroku/


After generating the csr, copy and past the csr code into where it prompts during (happens in workflow from 'activing ssl' on Namecheap).

- choose to validate with by adding a CNAME record (it's fastest)
- Then following the link to DCV editing so you can get the record.
- The record has your key (aka Host) and value for the CNAME
- Namespace may appended the domain name to the end of the key/host field- if so delete the domain appended.

### Retreive ssl/tls certificate (crt)

You'll get the certificate in an email (probably thru sectigo). You can also use the download link in the ssl certificates page on namecheap.

### Prepare certificates

Download from sectgo email (not from namecheap)

```cat your_domain.crt your_domain.ca-bundle >> your_domain_chain.crt```

Do not use the online tool they recommend. It doesn't appear to be correct.

Example uploading a directory with ssl certificate and info.

```
sudo rsync -avze "ssh -i /path/to/turbosrc-ngnix.pem" turbosrc-nginx-ssl-info ec2-user@<ipAddr or domain name>:/home/ec2-user
```

### Example folder paths of ssl certificates and info


### Example nginx config file

### Launch ngnix

Check the ngnix config file

```
nginx -t
```

Restart nginx
```
sudo systemctl restart nginx
```

or reload

```
sudo nginx -s reload
```
