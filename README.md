# FastAPI Monolith Docker Boilerplate by PLANEKS

📌 Insert here the project description. Also, change the caption of
the README.md file with name of the project.

## How to create the project

📌 Delete this section after creating new project.

Download the last version of the boiler plate from the repository: https://github.com/planeks/fastapi-monolith-boilerplate

You can download the ZIP archive and unpack it to the directory, or clone the repository (but do not forget to clean the Git history in that case). 

## 🐳 Install Docker and Docker Compose

For the local computer we recommend using Docker Desktop. 
You can download it from the official site: https://www.docker.com/products/docker-desktop

There are versions for Windows, Linux and Mac OS.

For the server installation you need the Docker Engine and Docker Compose. 
Use the following commands to install Docker on Ubuntu Linux:

```shell
# Add Docker's official GPG key:
$ sudo apt-get update
$ sudo apt-get install ca-certificates curl
$ sudo install -m 0755 -d /etc/apt/keyrings
$ sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
$ sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
$ echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
$ sudo apt-get update
$ sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

> If you are using another Linux distribution, please, check the official documentation: https://docs.docker.com/engine/install/

Test if Docker is installed correctly:

```shell
$ sudo systemctl status docker
```

Add the current user to the `docker` group (to avoid using `sudo`):

```shell
$ sudo usermod -aG docker ${USER}
```

## 🔨Setup the project locally

You need to run the project locally during the development. First of all, copy the `dev.env` file to the `.env` file in the same directory.

```shell
$ cp .env.example .env
```

Open the `.env` file in your editor and specify the settings:

```shell
POSTGRES_DB=boilerplate
POSTGRES_USER=boilerplate
POSTGRES_PASSWORD=boilerplate
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
SECRET_KEY="<secret>"
APP_HOST=localhost
APP_PORT=8000
APP_RELOAD=true
API_PREFIX="/api"
CORS_ORIGINS="*"
```

📌 Generate the secret key for the project and paste it to the `.env` file.
Also, generate the reasonably good password for the database user.

We strongly recommend creating some local domain in your `/etc/hosts` file to work with the project :

```
127.0.0.1   myproject.local
```

Use the following command to build the containers:

```shell
$ docker compose -f docker-compose.dev.yml build
```

Use the next command to run the project in detached mode:

```shell
$ docker compose -f docker-compose.dev.yml up -d
```

Use the following command to run `bash` inside the container.

```shell
$ docker compose -f docker-compose.dev.yml exec fastapi bash
```

Or, you can run the temporary container:

```shell
$ docker compose -f docker-compose.dev.yml run --rm fastapi bash
```

## 🖥️ Deploying the project to the server

📌 Modify this section according to the project needs.

### Configure main user

We strongly recommend deploying the project with an unprivileged user instead of `root`.

> The next paragraph describes how to create new unprivileged users to the system. If you use AWS EC2 for example, it is possible that you already have such kind of user in your system by default. It can be named `ubuntu`. If such a user already exists you do not need to create another one.

You can create the user (for example `webprod`) with the following command:

```shell
$ adduser webprod
```

You will be asked for the password for the user. You can use [https://www.random.org/passwords/](https://www.random.org/passwords/) to generate new passwords.

Add the new user `webprod` to the `sudo` group:

```bash
$ usermod -aG sudo webprod
```

Now the user can run a command with superuser privileges if it is necessary.

Usually, you shouldn't log in to the server with a password. 
You should use the ssh key. If you don't have one yet you can create 
it easily on your local computer with the following command:

```bash
$ ssh-keygen -t rsa
```

> The command works on Linux and Mac OS. If you are using Windows you can use 
> PuTTYgen to generate the key.

You can find the content of your public key with the next command:

```bash
$ cat ~/.ssh/id_rsa.pub
```

Now, go to the server and temporarily switch to the new user:

```bash
$ su - webprod
```

Now you will be in your new user's home directory.

Create a new directory called `.ssh` and restrict its permissions with the following commands:

```bash
$ mkdir ~/.ssh
$ chmod 700 ~/.ssh
```

Now open a file in `.ssh` called `authorized_keys` with a text editor. We will use `nano` to edit the file:

```bash
$ nano ~/.ssh/authorized_keys
```

> If your server installation does not contain `nano` then you can use `vi`. Just remember `vi` has different modes for editing text and running commands. Use `i` key to switch to the *insert mode*, insert enough text, and then use `Esc` to switch back to the *command mode*. Press `:` to activate the command line and type `wq` command to save file and exit. If you want to exit without saving the file just use `q!` command.

Now insert your public key (which should be in your clipboard) by pasting it into the editor. Hit `CTRL-x` to exit the file, then `y` to save the changes that you made, then `ENTER` to confirm the file name (in the case if you use `nano` of course).

Now restrict the permissions of the `authorized_keys` file with this command:

```bash
$ chmod 600 ~/.ssh/authorized_keys
```

Type this command once to return to the root user:

```bash
$ exit
```

Now your public key is installed, and you can use SSH keys to log in as your user.

Type `exit` again to logout from `the` server console and try to log in again as `webprod` and test the key based login:

```bash
$ ssh webprod@XXX.XXX.XXX.XXX
```

If you added public key authentication to your user, as described above, your private key will be used as authentication. Otherwise, you will be prompted for your user's password.

Remember, if you need to run a command with root privileges, type `sudo` before it like this:

```bash
$ sudo command_to_run
```

### Install dependencies

We also recommend to install a necessary software:

```bash
$ sudo apt install -y git wget tmux htop mc nano build-essential
```

🐳 Install Docker and Docker Compose as it was described above.

Create a new group on the host machine with `gid 1024` . It will be important for allowing to setup correct non-root permissions to the volumes.

```bash
$ sudo addgroup --gid 1024 fastapi
```

> NOTE. If you cannot use the GID 1024 for any reason, you can choose other value but edit the `Dockerfile` as well.

And add your user to the group:

```bash
$ sudo usermod -aG fastapi ${USER}
```

### Generate deploy key

Now, we need to create SSH key for deploy code from the remote repository 
(if you use GitHub, Bitbucket, GitLub, etc.).

    $ ssh-keygen -t rsa

Show the public key:

    $ cat ~/.ssh/id_rsa.pub

Then go to the project's settings of your project on source code hosting (if you use Bitbucket than go to "Access keys" section, if GitHub than search "Deployment keys" section) and add the key there.

> It is a list of keys which allows the read-only access to the repository. It is very important that such kind of keys does not affect our user quota. Also, it allows doing not use the keys of our developers.

### Clone the project

Create the directory for projects and clone the source code:

```bash
$ mkdir ~/projects
$ cd ~/projects
$ git clone <git_remote_url>
```

📌 Use your own correct Git remote directory URL.

Then you need to create the `.env` file with proper settings. You can use the `.env.example` as a template to create it

> ⚠️ Generate strong secret key and passwords. It is very important.

Now you can run the containers:

```bash
$ docker compose -f docker-compose.yml build
$ docker compose -f docker-compose.yml up -d
```

## Backup script

Configure the backup script to make regular backups of the database. You can call it `backup.sh` and put it to 
the `/home/webprod` directory.

Create the directory for backups:

```bash
$ mkdir /home/webprod/backups
```

The idea is to make a database dump, add the project files including the `.env` file and `media` directory to the archive.
Those archives will be stored locally to the `backups` directory. The script will remove the local archives older than 5 days.
We also strongly recommend to store the archives on the remote storage. 
You can use AWS S3 or DigitalOcean Spaces. You can use the `s3cmd` utility for that. Install it with the following command:

```bash
$ sudo apt install s3cmd
```

Configure the `s3cmd` utility with the following command:

```bash
$ s3cmd --configure
```

The `backup.sh` script should contain the next code:

```bash
#!/bin/bash
TIME_SUFFIX=`date +%Y-%m-%d:%H:%M:%S`
cd /home/webprod/projects/newprojectname
docker compose -f docker-compose.yml exec -T postgres backup
DB_DUMP_NAME=`docker compose -f docker-compose.yml exec -T postgres backups | head -n 3 | tail -n 1 | tr -s ' ' '\n' | tail -1`
docker cp newprojectname_postgres_1:/backups/$DB_DUMP_NAME /home/webprod/backups/
tar --exclude='media/thumbs' -zcvf /home/webprod/backups/newprojectname-$TIME_SUFFIX.tar.gz /home/webprod/projects/newprojectname/data/prod/media /home/webprod/projects/newprojectname/.env /home/webprod/projects/newprojectname/src /home/webprod/backups/$DB_DUMP_NAME
s3cmd put /home/webprod/backups/newprojectname-$TIME_SUFFIX.tar.gz s3://newprojectname-backups/staging/
find /home/webprod/backups/*.gz -mtime +5 -exec rm {} \;
docker compose -f docker-compose.yml exec -T postgres cleanup 7
```

📌 Modify the script according to the project needs. Check the directories and file names.

Try to run the script manually and than add it to the `crontab` to run it regularly.

```bash
$ sudo crontab -e
```

Add the next line

```bash
0 1 * * *       /home/webprod/backup.sh >> /home/webprod/backup.log 2>&1
```

## Restore project from backup

First, you need to unzip the archive for the particular date. If the archive is stored on the remote storage you need to download it first.

Than, if you need to restore source code, `.env` or `media` files you can just copy them to the proper directories.

If you need to restore the database you need to do the following steps.

Copy the database dump to the `backups` directory:

```bash
$ docker cp <dump_name> newprojectname_postgres_1:/backups/
```

Stop the app containers that are using the database (`fastapi`, etc.)

```bash
$ docker compose -f docker-compose.yml stop fastapi
``` 

Restore the database:

```bash
$ docker compose -f docker-compose.yml exec -T postgres restore <dump_name>
```

Run the app containers again:

```bash
$ docker compose -f docker-compose.yml up -d django celeryworker
```

## Cleaning Docker data

Also, you can setup the Cron jobs to schedule cleaning unnecessary Docker data.

```bash
$ sudo crontab -e
```

Add the next lines

```bash
0 2 * * *       docker system prune -f >> /home/webprod/docker_prune.log 2>&1
```

📌 If this document does not contain some important information, please, add it.