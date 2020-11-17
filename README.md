# Django/React template

Testing
-----

##### Backend

Backend tests are implemented with [`pytest`](https://docs.pytest.org/en/latest/)
via [`tox`](https://tox.readthedocs.io/en/latest/). From the host system you need
to execute the command inside of the `django` container so `docker
exec -it django tox -e pytest` will accomplish this.

Linting
-----

##### Backend

We use [`black`](https://pypi.org/project/black/) to autoformat our code and it
is invoked with `docker exec -it django tox -e black`.

Linting is done using [`flake8`](https://pypi.org/project/flake8/) and invoked with
`docker exec -it django tox -e flake8`.

##### Frontend

We use [`prettier`](https://prettier.io/) to autoformat our code and [`eslint`](https://eslint.org/) to lint it.
Using the fantastic `eslint-prettier` plugin you can lint the code
using `docker exec -it react npm run lint` and `docker exec -it react npm run lint-fix` to apply the
formatting to that lint result.

Windows Installation
-----

Firstly, install [`Docker for Windows`](https://docs.docker.com/docker-for-windows/install/) and follow the steps. You may need to check for updates for Windows if your installation fails. Once this installs, you want to get [`Ubuntu`](https://ubuntu.com/download/desktop). This will allow you to use `bash` commands, which I prefer over using `PowerShell`. If you use Visual Studio Code (which I recommend), you'll then want to install the [`Remote - WSL`](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-wsl) extension, allowing you to run a terminal in Ubuntu while using your VSCode editor.

Make sure you check whether `Ubuntu` is set as a WSL 2 Distro by going to Docker's Settings, heading into the `Resources` tab, clicking on `WSL Integration`, and confirming that `Ubuntu`'s integration is enabled.

After installing everything, you should be good to go!

Build
-----

##### The Environment

Save this as a file called `.env` and put it in the project root next to
`docker-compose.py`:

```bash
DB_NAME=somename
DB_PASSWORD=somepassword
DB_USER=someuser
DB_HOST=postgres
DB_PORT=5432

DEBUG=1
```

This will ensure that both postgres and django are using the same credentials
for the database.

##### First Run

`mkdir -p ~/srv/docker/template-postgresql/data` to create the directory for your Postgres volume.

`docker-compose build && docker-compose up -d` build and bring the containers
up.

`docker-compose logs -f` follow the docker logs.


##### Docker Commands

`docker-compose build` builds the containers.

`docker-compose up` brings up the containters (-d flag brings them up detached)

`docker-compose logs -f` view logs for detached running containers.

`docker-compose down` bring down the containers.

##### Docker Tips

Note: The container names you need are in the `docker-compose.yml` file.

Note: The containers are reading from the host filesystem so editing files
locally will propagate changes inside the contaner.

`docker-compose stop <container name>` stops a particular container.

`docker exec -it <container name> <command to execute inside the container>`
executes scripts inside container.

Ex: `docker exec -it django /bin/bash` loads you into a bash shell inside the
django container.

Ex: `docker exec -it django python manage.py shell` puts you in the django
shell.

File Structure
-----

##### Docker

All Docker container configuration files of any kind can be found in the `conf` folder.
The folder contains subfolders with names identical to the container name in
`docker-compose.yml`. In this way it is obvious what `Dockerfile` and/or startup
script a given container will be using. I also include other relevant files like
`requirements.txt` in `conf/django` as the `django` container is actually the
container that cares about requirements. In general our goal is to use startup
scripts whenever possible as they are extensible and mean less editing of the
`docker-compose.yml`.

##### Backend

This project follows typical django style contentions with the main project
folder inside `core`; this contains the `settings.py` and other relevant folders.

##### Frontend

The current design is to have a folder in the project root called `front` to
contain all react/frontend files. This folder has two subdirectories called
`src` which contains all `.js/.jsx` and a folder called `public` which contains
any `css/html/png/jpg/etc`, basically the static assets.
