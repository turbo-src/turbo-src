# AWS Linux ec2 instance

Select 30GB for root volume. Should be in free tier range.

Update system.

```
sudo yum update -y
```

## Install git

sudo yum install git -y

## Setup docker

Install docker

```
sudo yum install docker
```

Start docker

```
sudo service docker start
```

Enable running docker without sudo.

```
sudo usermod -a -G docker ec2-user
```

You'll have to logout and back into the shell.


We didn't choose to start docker on startup. But we should do that.

### Other sources

**install latest version of docker**

Docker package versions in the default repositories of many Linux distributions might not always keep up with the latest versions released by Docker. If you installed Docker from the default repositories of your Linux distribution, you may have an older version. To upgrade Docker and ensure you always have the latest version, you need to set up Docker's official repositories on your system and install from them.

Here is the general process to upgrade Docker on a CentOS or RHEL system:

Uninstall the older version of Docker:

```
sudo yum remove docker docker-client docker-client-latest docker-common docker-latest docker-latest-logrotate docker-logrotate docker-engine
```

This command will not remove images, containers, volumes, or user-created configuration files on your host. It's just removing the Docker package and associated dependencies. If you want to save and load Docker data, check Docker documentation on docker save and docker load.

Set up the Docker repository on your system. You need to first update the yum package index and then install a few packages that Docker needs:

```
sudo yum update -y
sudo yum install -y yum-utils device-mapper-persistent-data lvm2
```

Then, you can add the Docker repository with the following command:

```
sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
```

Install the latest version of Docker CE (Community Edition) using the following command:

```
sudo yum install -y docker-ce docker-ce-cli containerd.io
Start Docker and enable it to start on boot:
```

```
sudo systemctl start docker
sudo systemctl enable docker
```
Verify that Docker CE is installed correctly by running the hello-world image:

```
sudo docker run hello-world
```

This command downloads a test image and runs it in a container. When the container runs, it prints an informational message and exits.

Please note that the exact names of the packages might change in the future as Docker evolves, so you should always check Docker's official documentation for the most accurate information.

**Even more sources**

Go to section Installing Docker on Amazon Linux 2
https://docs.aws.amazon.com/AmazonECS/latest/developerguide/create-container-image.html

But here it says to do something else, which is different than above

https://gist.github.com/npearce/6f3c7826c7499587f00957fee62f8ee9

Make sure to exit terminal session then rejoin. Otherwise changes for 'no sudo' don't go into effect.

## Docker-compose install

**Download binary.**


Do this one.

```
sudo curl -L https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
```

or you can install a older version of docker-compose like this but this resulted in breaking turbosrc.

```
sudo curl -L https://github.com/docker/compose/releases/download/1.22.0/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
```



I install the old one as `yum` docker v20.10.23 is an old one.

Give permissions.

```
sudo chmod +x /usr/local/bin/docker-compose
```

See version and verify it's installed.

```
docker-compose version
```
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