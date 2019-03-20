# Redcloud
![](https://img.shields.io/badge/Python-3+-brightgreen.svg) [![](https://img.shields.io/badge/Usable_Templates-35-brightgreen.svg)](https://github.com/khast3x/redcloud/blob/master/nginx-templates/templates.yml) ![](https://img.shields.io/github/issues-raw/khast3x/redcloud.svg?style=social)

*Weather report. Cloudy with a chance of shells!*  

Early release. Follow me on [Twitter](https://twitter.com/kh4st3x) to stay updated on Redcloud's development   
:information_desk_person::cloud::shell::seedling:

___
[Introduction](#introduction) - [Quick Start](#quick-start) - [Redcloud Architecture](#redcloud-architecture) - [Accessing containers from the terminal](#accessing-containers-from-the-terminal) - [Portainer App Templates](#portainer-app-templates)
    - [Traefik reverse-proxy](#traefik-reverse-proxy)
    - [Redcloud security considerations](#redcloud-security-considerations) - [Troubleshooting](#troubleshooting) - [Use-cases](#use-cases) - [Screenshots](#screenshots) - [Hosting Redcloud](#hosting-redcloud)  - [Inspirations & Shout-outs](#inspirations--shout-outs)
___

## Introduction

Redcloud is a powerful and user-friendly toolbox for deploying a fully featured **Red Team Infrastructure** using Docker. Deploys in minutes. Use and manage it with its [polished web interface](#screenshots).  

Ideal for your penetration tests, shooting ranges, red teaming and bug bounties!  
  
  
Self-host your attack infrastructure painlessly, deploy your very own live, scalable and resilient offensive infrastructure in a matter of minutes.

___


## Features

* Deploy Redcloud locally or remotely using the built-in SSH functions, and even docker-machine.
* Deploy Metasploit, Empire, GoPhish, vulnerable targets, a fully stacked Kali, and many more with a few clicks.
* Monitor and manage your infrastructure with a beautiful web interface.
* Deploy redirections, socks or Tor proxy for all your tools.
* Painless network management and volume sharing.
* User and password management.
* Web terminal 
* Overall very comfy :hatching_chick:

___

## Quick Start


```bash
# If deploying using ssh
> cat ~/.ssh/id_rsa.pub | ssh root@your-deploy-target-ip 'cat >> .ssh/authorized_keys'

# If deploying using docker-machine, and using a machine named "default"
> eval (docker-machine env default)

# Check your Python version
# Use python3 if default python version is 2.x

> python --version

```

```bash
> git clone https://github.com/khast3x/redcloud.git
> cd redcloud
> python redcloud.py
```

Redcloud uses `PyYAML` to print the list of available templates. It's installed by default on most systems.  
If not, simply run:
```bash
# Use pip3 if default python version is 2.x
> pip install -r requirements.txt
```

The Redcloud menu offers 3 different deployment methods:
1. **Locally**
2. **Remotely, using ssh**. Requires having your public key in your target's `authorized_keys` file.
3. **Remotely, using docker-machine**. Run the `eval (docker-machine env deploy_target)` line to preload your env with your docker-machine, and run `redcloud.py`. Redcloud should automatically detect your docker-machine, and highlight menu items relevant to a docker-machine deployment.
<p align="center">
  <img src="https://i.imgur.com/2rdYzby.png" width="540" title="Redcloud menu">
</p>

**Redcloud deployment workflow is as follows:**
1. Clone/Download Redcloud repository.
2. Launch `redcloud.py`.
3. Choose deployment candidate from the menu (local, ssh, docker-machine).
4. `redcloud.py` automatically:
   *  checks for `docker` & `docker-compose` on target machine.
   *  installs `docker` & `docker-compose` if absent.
   *  deploys the web stack on target using `docker-compose`.
5. Once deployment is complete, `redcloud.py` will output the URL. Head over to https://your-deploy-machine-ip/portainer.
6. Set username/password from the web interface.
7. Select the endpoint (the only one on the list).
8. Access the templates using the "App Templates" menu item on the left :rocket:

**App Template deployment is as follows:**
1. Choose template.
2. If you wish to add additional options, select "+ Show advanced options".
3. Add port mapping, networking options, and volume mapping as you see fit.
4. Select "Deploy the container".
5. Portainer will launch the container. It may take a few minutes if it needs to fetch the image. If your server is in a data center, this step will be very fast.
6. Container should be running :rocket:
7. Portainer will redirect you to the "Containers" page. From there, you can:
   a. View live container logs.
   b. Inspect container details (`docker inspect`).
   c. View live container stats (memory/cpu/network/processes).
   d. Use a web shell to interact with your container.
   e. Depending on the App Template, use either `bash` or `sh`. Choose accordingly from the drop-down menu.

___

**Briefly,**

`redcloud.py` deploys a [Portainer](https://www.portainer.io/) stack, **preloaded with many tool templates for your offensive engagements**, powered by Docker. Once deployed, use the [web interface](#screenshots) to manage it. Easy remote deploy to your target server using the system `ssh` or even `docker-machine` if that's your thing.
  

* :rocket: Ever wanted to spin up a Kali in a cloud with just a few clicks?  
* :package: Have clean silos between your tools, technics and stages?  
* :ambulance: Monitor the health of your scans and C2?  
* :fire: Skip those sysadmin tasks for setting up a phishing campaign and get pwning faster?  
* :smiling_imp: Curious how you would build *the* ideal attack infrastructure?


Use the web UI to monitor, manage, and **interact with each container**. Use the snappy web terminal just as you would with yours. Create volumes, networks and port forwards using Portainer's simple UI.

Use all your favorite tools and technics with the power of data-center-grade internet.

___

* :book: **Table of contents**
  - [Redcloud](#redcloud)
    - [Introduction](#introduction)
    - [Features](#features)
    - [Quick Start](#quick-start)
    - [Details](#details)
      - [Redcloud Architecture](#redcloud-architecture)
      - [Networks](#networks)
      - [Volumes](#volumes)
      - [Accessing containers from the terminal](#accessing-containers-from-the-terminal)
      - [Accessing files](#accessing-files)
      - [SSL Certificates](#ssl-certificates)
      - [Stopping Redcloud](#stopping-redcloud)
      - [Portainer App Templates](#portainer-app-templates)
      - [Traefik reverse-proxy](#traefik-reverse-proxy)
      - [Redcloud security considerations](#redcloud-security-considerations)
    - [Tested deployment candidates](#tested-deployment-candidates)
    - [Troubleshooting](#troubleshooting)
    - [Use-cases](#use-cases)
    - [Screenshots](#screenshots)
    - [Contribution guideline](#contribution-guideline)
    - [Hosting Redcloud](#hosting-redcloud)
    - [Inspirations & Shout-outs](#inspirations--shout-outs)

___

## Details

### Redcloud Architecture

* `redcloud.py`: Starts/Stops the Web interface and App Templates, using Docker and Portainer.
* `portainer`: Portainer web interface.
* `traefik`: Traefik reverse-proxy container to the web interface, api and files containers. Some templates have pre-configured routes for convenience. See the `templates.yml`. 
* `nginx-templates`: NGINX server container that feeds the App Templates. Lives in an "inside" network.
* `redcloud_cert_gen_1`: The [omgwtfssl](https://github.com/paulczar/omgwtfssl) container that generates the SSL certificates using best practices.
* https://your-server-ip/portainer: Redcloud Web interface once deployed.

### Networks

Redcloud makes it easy to play around with networks and containers.  
You can create additional networks with different drivers, and attach your containers as you see fit. Redcloud comes with 2 networks, `redcloud_default` and `redcloud_inside`.

### Volumes

You can share data between containers by sharing volumes. Redcloud comes with 3 volumes:

* `certs`: Container with the certificates generated by [omgwtfssl](https://github.com/paulczar/omgwtfssl).
* `files`: Standard file sharing volume. For now, the files are available when browsing https://your-server-ip/files, and are served by the Traefik reverse-proxy container directly from the `files` volume. A typical use-case is to attach the volume to a Metasploit container, generate your payload directly into the `files` volume. You can now serve your fresh payload directly through the Traefik to file server route.
* `logs`: Available for logs, served by the file-server too. Access requires basic auth. Default is `admin:Redcloud`.

### Accessing containers from the terminal

If you wish to stay in your terminal to work with the deployed containers, its very easy using Docker. Keep these things in mind:
* Most containers have `bash`, but some use `sh` instead
* All Redcloud App Templates container names start with `red_`, such as `red_msf-postgresql`
* With Docker, you can either use `docker exec` or `attach` to interact with a container
  * `exec` is preferred as it creates a new process
  * `attach` lands you straight on the running process, potentially killing your running container
* If running Redcloud:
  * Locally or using `docker-machine`, simply type these in your local shell
  * Using `ssh`, first ssh into your deployment target to run the following commands

To start interacting with the desired deployed container:  
```bash
> docker exec -it red_container-name /bin/bash
root@70a819ef0e87:/#
```

If you see the following message, it means `bash` is not installed. In that case simply replace `/bin/bash` with `/bin/sh`:

```bash
> docker exec -it red_container-name /bin/bash
OCI runtime exec failed: exec failed: container_linux.go:344: starting container process caused "exec: \"/bin/bash\": stat /bin/bash: no such file or directory": unknown

> docker exec -it red_container-name /bin/sh
#
```

To use `docker attach`, simply run:
```bash
> docker attach red_container-name
```
If using `attach`, the container needs to be started in `interactive mode`, so as to land in a interactive shell.


### Accessing files

Point your browser to `https://your-redcloud-ip`.  
Please refer to the `files` volume for more information.

### SSL Certificates

Redcloud generates a new *unsigned* SSL certificate when deploying.  
The certificate is generated by [omgwtfssl](https://github.com/paulczar/omgwtfssl), implementing most best practices.
Once generated:
> It will dump the certificates it generated into /certs by default and will also output them to stdout in a standard YAML form, making them easy to consume in Ansible or other tools that use YAML. 

Certificates are stored in a shared docker volume called `certs`. Your containers can access this volume if you indicate it in "+ Advanced Settings" when deploying it. The Traefik reverse-proxy container fetches the certificates directly from its configuration file. If you wish to replace these certificates with your own, simply replace them on this volume.

It also means you can share the generated certificates into other containers, such Empire or Metasploit for your reverse callbacks, or for a phishing campaign.
Most SSL related configurations can be found in `traefik/traefik.toml` or the `docker-compose.yml` file.


### Stopping Redcloud

You can stop Redcloud directly from the menu.  
**Deployed App templates need to be stopped manually before stopping Redcloud.** You can stop them using the Portainer web interface, or `docker rm -f container-name`.  
If you wish to force the Portainer containers running Redcloud to stop, simply run `docker-compose kill` inside the `redcloud/` folder.
The *local* and *docker-machine* stop option is the same, thus they are combined in the same option.


### Portainer App Templates

Redcloud uses Portainer to orchestrate and interface with the Docker engine. Portainer in itself is a fantastic project to manage Docker deployments remotely. Portainer also includes a very convenient [template system](https://portainer.readthedocs.io/en/stable/templates.html), which is the major component for our Redcloud deployment.  
Templates can be found in `./nginx-templates/templates.yml`. Portainer fetches the template file from a dedicated NGINX container (`nginx-templates`).

### Traefik reverse-proxy

 
Traefik is a wonderful "cloud-native edge router". It has replaced the previous NGINX reverse-proxy setup.  
A Traefik image is built during deployment, using the Dockerfile located in `traefik/Dockerfile`. It adds a `.htpasswd` with `admin:Redcloud` credentials.  

By default, deployment spawns the following routes:  
* `https://your-server-ip/portainer`
* `https://your-server-ip/files`
* `https://your-server-ip/api`

Authentications are based of the `.htaccess` data.

From the Traefik api web interface, you can view your deployed routes, monitor health, as well as real time metrics. Its very neat.

![gopher](https://raw.githubusercontent.com/containous/traefik/master/docs/content/assets/img/traefik.icon.png)  

You can add additional labels that tell Traefik where to route traffic, using:
* `traefik/traefik.toml` file
* `docker-compose.yml` file
* `templates.yml` file
* Portainer's web interface

 See the [official documentation](https://docs.traefik.io/basics/) for more information.

![api](https://i.imgur.com/gWaeykt.png)


### Redcloud security considerations

Redcloud deploys with a self-signed https certificate, and proxies all interactions with the web console through it.  
However, the default network exposes your containers' ports to the outside world.

You can:
* Add custom `labels` to create routes with Traefik. See the `docker-compose.yml` file for inspiration.
* Start an Ubuntu+noVNC (VNC through http) from template, add it to both an "inside" and "outside" network, and access exposed interfaces from inside.
* Add .htaccess configurations. Some are planned in further Redcloud development.

Additionally:  
* `docker` & `docker-machine` installations require root privileges. You can downgrade privilege requirements following [the official documentation](https://docs.docker.com/install/linux/linux-postinstall/).
* The install script is pulled directly from the official docker repositories.
* `redcloud.py` fetches Redcloud's public IP address using icanhazip.com.

___

## Tested deployment candidates

| Deploy Target |        Status       |
|:-------------:|:-------------------:|
| Ubuntu Bionic | :heavy_check_mark: |
| Ubuntu Xenial | :heavy_check_mark: |
| Debian Strech | :heavy_check_mark: |

___

## Troubleshooting

* Check your default python version with `python --version`. Redcloud needs python 3+.
* Use `python3` instead of `python` if on an older system.
* `redcloud.py` requires that deployment candidate have the public key in their `.ssh/authorized_keys`, and handles password-less authentication using the user's public key. This is the default configuration for most VPS workflows.
* docker-machine deployment requires the user to already have a running docker-machine on a cloud infrastructure (such as AWS, GCP, Linode and [many others](https://docs.docker.com/machine/drivers/)). Once deployed, simply run the `eval` command as illustrated above.
* `docker` & `docker-machine` installations require root privileges. You can downgrade privilege requirements following [the official documentation](https://docs.docker.com/install/linux/linux-postinstall/)
* If you don't see the "App Templates" menu item right after deploying, refresh the web page and make sure you're not at the endpoint selection menu.
* If you wish to create a new username/password combo, remove Portainer persistent data on deployment candidate: `rm -rf /opt/portainer/data`
* If you're running into python errors, you may need to install the `python3-distutils` package using `apt-get install python3-distutils` on debian/ubuntu base.
* If you get an error when deploying an App Template saying the "container name already exists", it's probably because you're trying to deploy the same App Template without having removed a previously deployed one. Simply remove the old container with the same name, or change the name of your new container.
* If something seems wrong with your container, the standard procedure is to check the container's logs from the web interface.
* If running a local deployment on OSX, `portainer` will be unable to use its default volume location `/opt/`. To solve this, open the `docker-compose.yml` file, replace `/opt/portainer/data:/data` with a folder with write-access, for example: `/tmp/portainer/:/data` and create the `/tmp/portainer` directory before running Redcloud.

___

## Use-cases

* Create your personal pentest-lab, and practice your hacking skills with friends and colleagues.
* Throw off the blue team by deploying honeypots. Can be one or one thousand honeypots thanks to containers!
* Deploy Metasploit or Empire, generate payload, served with nginx files.
* Launch Sniper, fetch logs using nginx files.
* Use the reverse proxy to cover Metasploit or Empire.
* Use an xss scanner on Juice shop.
* Launch scans behind your own Tor socks proxy.
* View .onion site using Tor socks + Ubuntu VNC.
* Advanced OSINT with Spiderfoot and a Tor container as proxy.

___

## Screenshots

* Template List + `redcloud.py` deploy
![](https://i.imgur.com/j8YFjtw.png)

* Deploying a container
![](https://i.imgur.com/QCR1yHp.png)


* Using Metasploit's `msfconsole` through the web interface
![](https://i.imgur.com/wUcFHbh.png)

___

## Contribution guideline

Any help is appreciated. This is a side project, so it's probably missing a few bolts and screws. Above all:
* Reporting or fixing Redcloud bugs & quirks.
* Adding templates. Please keep it clean, and from the creator's docker hub repository if possible.
* Adding documentation.
* Detailing use cases in blog articles. I'll add links to blog posts here, so please be sure to contact me if you make one! :v:
* Typos as issues. *(no pull requests please)*

___

## Hosting Redcloud

You can host a Redcloud on any Unix server that runs Docker.  
Redcloud is intended to be used in a cloud environment, such as a simple VPS with ssh, or even an AWS EC2, GCP, etc...

A large range of cloud providers offer **free credits** to get familiar with their services. Many lists and tutorials cover getting free hosting credits from major vendors. [This list is a good place to start](https://github.com/ripienaar/free-for-dev#iaas).

Regarding deployment method, I personally prefer working with [docker-machine](https://docs.docker.com/machine/overview/) as it becomes ridiculously easy to spawn new machines and manage them once you've got your cloud provider's [driver setup](https://docs.docker.com/machine/drivers/). If you prefer using `ssh`, be sure to take a look at evilsocket's [shellz](https://github.com/evilsocket/shellz) project to manage your keys and profiles.

___

## Inspirations & Shout-outs

* [Red Team Infrastructure Wiki](https://github.com/bluscreenofjeff/Red-Team-Infrastructure-Wiki) - bluscreenofjeff
* [Automated Red Team Infrastructure Guide](https://rastamouse.me/2017/08/automated-red-team-infrastructure-deployment-with-terraform---part-1/) - rastamouse
* [Safe Red Team Infrastructure](https://medium.com/@malcomvetter/safe-red-team-infrastructure-c5d6a0f13fac) - Tim MalcomVetter
* [Red Baron](https://github.com/Coalfire-Research/Red-Baron) - Coalfire Research
* [Rapid Attack Infrastructure](https://github.com/obscuritylabs/RAI) - Obscurity Labs
* [Decker](https://github.com/stevenaldinger/decker) - Steven Aldinger
* [HideNSeek](https://github.com/rmikehodges/hideNsneak) - Mike Hodges

___

*Finally, I'd love to integrate Cobalt Strike. Unfortunately, I don't see myself having the funds to invest in a license, so if you know someone who knows someone, I'm all ears* :innocent:
___

*If you wish to stay updated on this project:*

[![twitter](https://i.imgur.com/S79Nimd.png)](https://twitter.com/kh4st3x)
