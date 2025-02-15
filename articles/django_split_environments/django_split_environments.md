<!---------------------------- 
  TODO: t.o.c.
  TODO: add git pushes
  TODO: add headers
  TODO: config docker/compose  
----------------------------->

<!-- -----***[ configure-a-secure-django-project-with-docker-dual-environments ]*** ----- *** -->

---
# Configure a Secure Django Project with Docker: Dual Environments  


<br><br>


---
### Ensure Required System Tools  <!-- *** ---------- *** -- [ 1-ensure-required-system-tools ] -- *** ---------- *** -->
---

The following tools are required. Exact versions used in this guide are documented below, however, newer versions *should* work as well. Run the Verify Install CMD to verify if the tools are installed.

<br>

#### Verify installation of required tools:

| Package               | Verify Install CMD                         | Install Docs          |
|-----------------------|--------------------------------------------|-----------------------|
| python         3.12.4 | `python -V` <small>(upper 'V')</small> | [idroot.us](https://idroot.us/install-python-ubuntu-24-04/)       |
| docker         27.0.3 | `docker -v` <small>(lower 'v')</small> | [docs.docker.com](https://docs.docker.com/engine/install/ubuntu/) |
| docker-compose 2.28.1 | `docker-compose version`               | [docs.docker.com](https://docs.docker.com/compose/install/#scenario-two-install-the-compose-plugin) |

<br><br>


---
### Init Project Root Directory  <!-- *** ---------- *** -- [ 2-init-project-root-directory ] -- *** ---------- *** -->
---

The project root is the directory where our project will live. We'll name our project and project root directory `myproject`.

<br>

#### Create `./myproject` root:

```bash
#!/usr/bin/env bash

# `mdkir` --> `./myproject`
mkdir "./myproject"

```

<br>

#### Change directories to `./myproject`:

```bash
#!/usr/bin/env bash

# `cd` --> `./myproject`
cd myproject

```

<br><br>

---
### Init Virtual Environment  <!-- *** ---------- *** -- [ 3-init-virtual-environment ] -- *** ---------- *** -->
---

<br>

#### Inside `./myproject` create `./venv`:

```bash
#!/usr/bin/env bash

# `venv` --> `./venv`
python -m venv --copies --upgrade-deps "./venv"

```

<br>

#### Activate `./venv`:

```bash
#!/usr/bin/env bash

# `source` --> `./venv` active
source "./venv/bin/activate"

```

<br>

There's numurous ways to verify active virtual environments but the `sys.prefix` method is used here because it's reliable. 

Here's an excerpt from [python docs](https://docs.python.org/3/library/sys.html#sys.base_prefix):

> <b>sys.base_prefix</b> <br>
> Set during Python startup, before site.py is run, to the same value as prefix. If not running in a virtual environment, the values will stay the same; if site.py finds that a virtual environment is in use, the values of prefix and exec_prefix will be changed to point to the virtual environment, whereas base_prefix and base_exec_prefix will remain pointing to the base Python installation (the one which the virtual environment was created from).

<br>

#### Check for active virtual environment:

```bash
#!/usr/bin/env bash

# sys.prefix` IS NOT EQUAL `sys.base_prefix` -> `venv` active
python -c 'import sys; print("true") if sys.prefix != sys.base_prefix else print("false");'

```

The `python` call should return `true` if the virtual environment is activated.

<br>

#### Verify that the `python` command calls the `python` executable located inside our new virtual environment:

```bash
#!/usr/bin/env bash

# `type python` -> `python is /home/[LINUX_USERNAME]/projects/myproject/venv/bin/python`
type python

```

The wanted `python` executable is inside our new virtual environment e.g. `/home/[LINUX_USERNAME]/projects/myproject/venv/bin/python`. Avoid using system Python which is commonly found in `/usr/bin/python`, it's used for important processes, and shouldn't be played with.

<br><br>


---
### Ensure Django  <!-- *** ------------------------- *** -- [ ensure-django ] -- *** ------------------------- *** -->
---

<br>

#### Install Django:

```bash
#!/usr/bin/env bash

# `python -m pip` --> django
python -m pip install django

```

<br><br>


---
### Create Apps Diectory  <!-- *** ----------------- *** -- [ create-apps-directory ] -- *** ------------------ *** -->
---

<br>

#### Create the `./apps` directory for django apps and related files:

```bash
#!/usr/bin/env bash

# `mkdir` --> `./apps`
mkdir "./apps"

```

<br><br>


---
### Create Dot Env Directories   <!-- *** ----------------- *** -- [ create-apps-directory ] -- *** ------------------ *** -->
---

<br>

#### Create `./.envs`, `./.envs/.development` & `./.envs/.production` directories for secrets and environment variable related files:

```bash
#!/usr/bin/env bash

# `mkdir` --> `./.envs` AND `./.envs/.development` AND `./.envs/.production`
mkdir "./.envs" "./.envs/.development" "./.envs/.production"

```

<br><br>


---
### Create Config Directories
---

<br>

#### Start a new Django project to create the `./config` directory for settings and other related files:

```bash
#!/usr/bin/env bash

# `django-admin startproject` --> `./config`.
django-admin startproject "config" "."

```

<br>

#### Create `./config/settings`, `./config/settings/development` & `./config/settings/production`:

```bash
#!/usr/bin/env bash

# `mkdir` --> `./config/settings` AND `./config/settings/development` AND `./config/settings/production`
mkdir "./config/settings" "./config/settings/development" "./config/settings/production"

```

<br><br>


---
### Create Compose Directories
---

<br>

#### Create `./compose`, `./compose/development` & `./compose/production` directories for Docker and Docker-Compose related files.

```bash
#!/usr/bin/env bash

# `mkdir` --> `./compose` AND `./compose/development` AND `./compose/production`
mkdir "./compose" "./compose/development" "./compose/production"

```

<br><br>


---
### Create NGINX Directory
---

<br>

#### Create the `./compose/production/nginx` directory for nginx proxy related files.

```bash
#!/usr/bin/env bash

# `mkdir` --> `./compose/production/nginx`
mkdir "./compose/production/nginx"

```

<br><br>


---
### Create Requirements Directories
---

<br>

#### Create `./requirements`, `./requirements/development` & `./requirements/production` directories for package requirements related files:

```bash
#!/usr/bin/env bash

# `mkdir` --> `./requirements` AND `./requirements/development` AND `./requirements/production`
mkdir "./requirements" "./requirements/development" "./requirements/production"

```

<br><br>


---
### Create Git Files
---

We will create some base config files for `github` including `LICENSE.md` containing the MIT LICENSE. The MIT LICENSE is permissive and used because it's common and open-source rules. To use an alternative license, skip creating `./LICENSE` and add the alternative license to the project as soon as possible. 

Warning from [GitHub docs](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository):

> Note: If you publish your source code in a public repository on GitHub, according to the Terms of Service, other users of GitHub.com have the right to view and fork your repository. If you have already created a repository and no longer want users to have access to the repository, you can make the repository private. When you change the visibility of a repository to private, existing forks or local copies created by other users will still exist.

Help choosing a license can be found on [choosealicense.com](https://choosealicense.com/) and instructions for adding the license to a project can be found on [GitHub docs](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository).

<br>

#### Create `./.gitignore`, `./README.md` and `./LICENSE.md`:

```bash
#!/usr/bin/env bash

# `touch` --> `./.gitignore` AND `./README.md` AND `./LICENSE.md`
touch "./.gitignore" "./README.md" "./LICENSE.md"

```

<br><br>


---
### Create Dot Env Files
---

<br>

#### Create `./.envs/.development.env` & `"./.envs/.production.env`:

```bash
#!/usr/bin/env bash

# `touch` --> `./.envs/development/.dev.env` AND `./.envs/production/.prod.env`
touch "./.envs/development/.dev.env" "./.envs/production/.prod.env"

```

<br><br>


---
### Create Settings Files
---

<br>

#### Move `./config/settings.py` to `./config/settings/base.py` and create `./config/development/dev.settings.py` & `./config/production/prod.settings.py`:

```bash
#!/usr/bin/env bash

# `mv` --> `./config/settings.py` --> `./config/settings/base.settings.py`.
mv "./config/settings.py" "./config/settings/base.settings.py"

# `touch` --> `./config/development/dev.settings.py` AND `./config/production/prod.settings.py`
touch "./config/development/dev.settings.py" "./config/production/prod.settings.py"

```

<br><br>


---
### Create Dockerfile Files
---

<br>

#### Create `dev.Dockerfile` & `prod.Dockerfile`:

```bash
#!/usr/bin/env bash

# `touch` --> `./compose/development/dev.Dockerfile` AND `./compose/production/prod.Dockerfile`.
touch "./compose/development/dev.Dockerfile" "./compose/production/prod.Dockerfile"

```

<br><br>


---
### Create Docker-Compose Files
---

<br>

#### Create `./compose/development/dev.docker-compose.yml` & `./compose/production/prod.docker-compose.yml`:

```bash
#!/usr/bin/env bash

# `touch` --> `./compose/development/dev.docker-compose.yml` AND `./compose/production/prod.docker-compose.yml`.
touch "./compose/development/dev.docker-compose.yml" "./compose/production/prod.docker-compose.yml"

```

<br><br>


---
### Create NGINX Config File
---

<br>

#### Create `./compose/production/nginx.conf`:

```bash
#!/usr/bin/env bash

# `touch` --> `./compose/production/nginx.conf`.
touch "./compose/production/nginx.conf"

```

<br><br>


---
### Create Requirements Files
---

<br>

#### Create `./requirements/development/dev.requirements.txt` & `./requirements/production/prod.requirements.txt`:

```bash
#!/usr/bin/env bash

# `touch` --> `dev.requirements.txt` AND `prod.requirements.txt`.
touch "./requirements/development/dev.requirements.txt" "./requirements/production/prod.requirements.txt"

```

<br><br>


---
### Configure Git Files
---

<br>

#### Open `./.gitignore`:

```bash
#!/usr/bin/env bash

# Open `.gitignore` with `$EDITOR`, or your choice of editor e.g. `nano`, `vim`, `subl` etc.
"${EDITOR}" "./.gitignore"

```

<br>

#### Update `./.gitignore`:

```txt
#--------------------------------------------------------------------#
#   Open-Source `.gitignore` template for Python.                    #
#   https://github.com/github/gitignore/blob/main/Python.gitignore   #
#--------------------------------------------------------------------#

# ./.gitignore

# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
#  Usually these files are written by a python script from a template
#  before PyInstaller builds the exe, so as to inject date/other infos into it.
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/
cover/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
.pybuilder/
target/

# Jupyter Notebook
.ipynb_checkpoints

# IPython
profile_default/
ipython_config.py

# pyenv
#   For a library or package, you might want to ignore these files since the code is
#   intended to run in multiple environments; otherwise, check them in:
# .python-version

# pipenv
#   According to pypa/pipenv#598, it is recommended to include Pipfile.lock in version control.
#   However, in case of collaboration, if having platform-specific dependencies or dependencies
#   having no cross-platform support, pipenv may install dependencies that don't work, or not
#   install all needed dependencies.
#Pipfile.lock

# poetry
#   Similar to Pipfile.lock, it is generally recommended to include poetry.lock in version control.
#   This is especially recommended for binary packages to ensure reproducibility, and is more
#   commonly ignored for libraries.
#   https://python-poetry.org/docs/basic-usage/#commit-your-poetrylock-file-to-version-control
#poetry.lock

# pdm
#   Similar to Pipfile.lock, it is generally recommended to include pdm.lock in version control.
#pdm.lock
#   pdm stores project-wide configurations in .pdm.toml, but it is recommended to not include it
#   in version control.
#   https://pdm.fming.dev/latest/usage/project/#working-with-version-control
.pdm.toml
.pdm-python
.pdm-build/

# PEP 582; used by e.g. github.com/David-OConnor/pyflow and github.com/pdm-project/pdm
__pypackages__/

# Celery stuff
celerybeat-schedule
celerybeat.pid

# SageMath parsed files
*.sage.py

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/
# added
*.env
.envs/
.envs

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/

# pytype static type analyzer
.pytype/

# Cython debug symbols
cython_debug/

# PyCharm
#  JetBrains specific template is maintained in a separate JetBrains.gitignore that can
#  be found at https://github.com/github/gitignore/blob/main/Global/JetBrains.gitignore
#  and can be added to the global gitignore or merged into this file.  For a more nuclear
#  option (not recommended) you can uncomment the following to ignore the entire idea folder.
#.idea/

```

<br>

#### Open `./README.md`.

```bash
#!/usr/bin/env bash

# Open `README.md` with `$EDITOR`, or your choice of editor e.g. `nano`, `vim`, `subl` etc.
"${EDITOR}" "./README.md"

```

<br>

#### Update `./README.md`:

```md
<!-- *** ----- ***|Customizable README template | https://github.com/othneildrew/Best-README-Template |*** ---- *** -->

<a id="readme-top"></a>

<!-- *** --------------------------------------- ***| PROJECT LOGO |*** --------------------------------------- *** -->

<br />

<div align="center">
  <a href="https://github.com/ShellDisciple/linkedin_articles">
    <img src="https://avatars.githubusercontent.com/u/174848331?v=4" alt="Logo" width="80" height="80">
  </a>
  <h3 align="center">myproject</h3>
  <p align="center">
    A secure Django Backend featuring development/production split-environments.
    <br />
    <a href="https://github.com/ShellDisciple/linkedin_articles">| Docs |</a>
    <a href="https://github.com/ShellDisciple/linkedin_articles">View Demo |</a>
    <a href="https://github.com/ShellDisciple/linkedin_articles/issues/new?labels=bug&template=bug-report---.md">Report Bug |</a>
    <a href="https://github.com/ShellDisciple/linkedin_articles/issues/new?labels=enhancement&template=feature-request---.md">Request Feature |</a>
  </p>
</div>

<!-- *** -------------------------------------- ***| PROJECT SHIELDS |*** -------------------------------------- *** -->
<!-- ----------------- ***| https://www.markdownguide.org/basic-syntax/#reference-style-links |*** ----------------- -->

<center>
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]
</center>

<br />

<!-- *** ------------------------------------- ***| TABLE OF CONTENTS |*** ------------------------------------- *** -->

<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<br />

<!-- *** ------------------------------------- ***| ABOUT THE PROJECT |*** ------------------------------------ *** -->

<p style="float:right">(<a href="#readme-top">back to top</a>)</p>

## About The Project

Here's a blank template to get started: To avoid retyping too much info. Do a search and replace with your text editor for the following: `ShellDisciple`, `linkedin_articles`, `twitter_handle`, `ShellDisciple`, `email_client`, `email`, `project_title`, `project_description`

[![Product Screen Shot][product-screenshot]](https://example.com)

<br />

### Built With

[![Python][Python]][Python-Url]
[![Django][Django]][Django-url]
[![DjangoRESTFramework][DjangoREST]][DjangoREST-url]
[![Postgres][Postgres]][Postgres-url]
[![Docker][Docker]][Docker-url]
[![Nginx][Nginx]][Nginx-url]

<br />

<!-- *** -------------------------------------- ***| GETTING STARTED |*** ------------------------------------- *** -->

<p style="float:right">(<a href="#readme-top">back to top</a>)</p>

## Getting Started

This is an example of how you may give instructions on setting up your project locally.

<br />

### Prerequisites

1. `npm` package required: npm install npm@latest -g

<br />

### Installation

1. Get a free API Key at [https://example.com](https://example.com)
2. Clone the repo: `git clone https://github.com/ShellDisciple/linkedin_articles.git`
3. Install NPM packages: `npm install`

<br />

<!-- *** -------------------------------------- ***| USAGE EXAMPLES |*** -------------------------------------- *** -->

<p style="float:right">(<a href="#readme-top">back to top</a>)</p>

## Usage

Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.

_For more examples, please refer to the [Documentation](https://example.com)_

<br />

<!-- *** ------------------------------------------ ***| ROADMAP |*** ----------------------------------------- *** -->

<p style="float:right">(<a href="#readme-top">back to top</a>)</p>

## Roadmap

See the [open issues](https://github.com/ShellDisciple/linkedin_articles/issues) for a full list of proposed features (and known issues).

- [X] Feature 1
- [X] Feature 2
- [ ] Feature 3
    - [ ] Nested Feature 1
    - [ ] Nested Feature 2

<br />

<!-- *** --------------------------------------- ***| CONTRIBUTING |*** --------------------------------------- *** -->

<p style="float:right">(<a href="#readme-top">back to top</a>)</p>

## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Here's how to contribute:

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Top Contributors

<a href="https://github.com/ShellDisciple/linkedin_articles/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=ShellDisciple/linkedin_articles" alt="contrib.rocks image" />
</a>

<br />

<!-- *** ------------------------------------------ ***| LICENSE |*** ----------------------------------------- *** -->

<p style="float:right">(<a href="#readme-top">back to top</a>)</p>

## License

Distributed under the MIT License. See `./LICENSE.md` for more information.

<br />

<!-- *** ------------------------------------------ ***| CONTACT |*** ----------------------------------------- *** -->

<p style="float:right">(<a href="#readme-top">back to top</a>)</p>

## Contact

Your Name - [@twitter_handle](https://twitter.com/twitter_handle) - email@email.com

Project Link: [linkedin_articles](https://github.com/ShellDisciple/linkedin_articles)

<br />

<!-- *** -------------------------------------- ***| ACKNOWLEDGMENTS |*** ------------------------------------- *** -->

<p style="float:right">(<a href="#readme-top">back to top</a>)</p>

## Acknowledgments

* [SomeOrg](https://www.example.com)
* [Another Shout Out](https://www.example.com)

<br />

<!-- *** ---------------------------------- ***| MARKDOWN LINKS & IMAGES |*** --------------------------------- *** -->
<!-- *** ------------- ***| https://www.markdownguide.org/basic-syntax/#reference-style-links |*** ------------ *** -->

[contributors-shield]: https://img.shields.io/github/contributors/ShellDisciple/linkedin_articles.svg?style=for-the-badge
[contributors-url]: https://github.com/ShellDisciple/linkedin_articles/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/ShellDisciple/linkedin_articles.svg?style=for-the-badge
[forks-url]: https://github.com/ShellDisciple/linkedin_articles/network/members
[stars-shield]: https://img.shields.io/github/stars/ShellDisciple/linkedin_articles.svg?style=for-the-badge
[stars-url]: https://github.com/ShellDisciple/linkedin_articles/stargazers
[issues-shield]: https://img.shields.io/github/issues/ShellDisciple/linkedin_articles.svg?style=for-the-badge
[issues-url]: https://github.com/ShellDisciple/linkedin_articles/issues
[license-shield]: https://img.shields.io/github/license/ShellDisciple/linkedin_articles.svg?style=for-the-badge
[license-url]: https://github.com/ShellDisciple/linkedin_articles/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/ShellDisciple
[product-screenshot]: images/screenshot.png

[Python]: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54
[Python-Url]: https://www.python.org
[Postgres]:https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white
[Postgres-url]: https://www.postgresql.org
[Django]: https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white
[Django-url]: https://docs.djangoproject.com/en/5.1
[DjangoREST]: https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray
[DjangoREST-url]: https://www.django-rest-framework.org
[Docker]: https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white
[Docker-url]: https://www.docker.com
[Nginx]: https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white
[Nginx-url]: https://nginx.org

<br /><br />

```

<br>

#### Open `./LICENSE.md`:

```bash
#!/usr/bin/env bash

# Open `./LICENSE.md` with `$EDITOR`, or favorite editor e.g. `nano`, `vim`, `subl` etc.
"${EDITOR}" "./LICENSE.md"

```

<br>

#### Update `./LICENSE.md`:

```md
MIT License

Copyright (c) 2024 [GITHUB_USERMAME]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

```

<br><br>


---
### Configure Dot Env Files
---

<br>

#### Open `.dev.env`:

```bash
#!/usr/bin/env bash

# Open `.dev.env` with `$EDITOR`, or your choice of editor e.g. `nano`, `vim`, `subl` etc.
"${EDITOR}" "./.envs/.development/.dev.env"

```

<br>

#### Update `.dev.env`:

```bash

DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=postgres://postgres:postgres@db:5432/postgres

```

<br>

#### Open `.prod.env`:

```bash
#!/usr/bin/env bash

# Open `.prod.env` with `$EDITOR`, or your choice of editor e.g. `nano`, `vim`, `subl` etc.
"${EDITOR}" "./.envs/production/.prod.env"

```

<br>

#### Update `.prod.env`:

```bash

DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=postgres://postgres:postgres@db:5432/postgres

```

<br><br>


---
### Configure Dockerfile Files
---

<br>

#### Open `./compose/development/dev.Dockerfile`:

```bash
#!/usr/bin/env bash

# Open `dev.Dockerfile` with `$EDITOR`, or your choice of editor e.g. `nano`, `vim`, `subl` etc.
"${EDITOR}" "./compose/development/dev.Dockerfile"

```

<br>

#### Update `./compose/development/dev.Dockerfile`:

```dockerfile
# ./compose/development/dev.Dockerfile

FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

```

<br>

#### Open `./compose/production/prod.Dockerfile`:

```bash
#!/usr/bin/env bash

# Open `prod.Dockerfile` with `$EDITOR`, or your choice of editor e.g. `nano`, `vim`, `subl` etc.
"${EDITOR}" "./compose/production/prod.Dockerfile"

```

<br>

#### Update `./compose/production/prod.Dockerfile`:

```dockerfile
# ./compose/production/prod.Dockerfile

#...

```

<br><br>


---
### Configure Docker-Compose Files
---

<br>

#### Open `./compose/development/dev.docker-compose.yml`:

```bash
#!/usr/bin/env bash

# Open `dev.docker-compose.yml` with `$EDITOR`, or your choice of editor e.g. `nano`, `vim`, `subl` etc.
"${EDITOR}" "./compose/development/dev.docker-compose.yml"

```

<br>

#### Update `./compose/development/dev.docker-compose.yml`:

```yaml
# ./compose/development/dev.docker-compose.yml
version: '3.8'

services:
  web:
    build:
      context: .
      dockerfile: dev.Dockerfile
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    env_file: .env
    depends_on:
      - db

  db:
    image: postgres:13
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    env_file: .env

volumes:
  postgres_data:

```

<br>

#### Open `./compose/production/prod.docker-compose.yml`:

```bash
#!/usr/bin/env bash

# Open `prod.docker-compose.yml` with `$EDITOR`, or your choice of editor e.g. `nano`, `vim`, `subl` etc.
"${EDITOR}" "./compose/production/prod.docker-compose.yml"

```

<br>

#### Update `./compose/production/prod.docker-compose.yml`:

```yaml
# ./compose/production/prod.docker-compose.yml
version: '3.8'

services:
  web:
    build:
      context: ../..
      dockerfile: prod.Dockerfile
    command: gunicorn config.wsgi:application --bind 0.0.0.0:8000
    volumes:
      - ../../:/app
    ports:
      - "8000:8000"
    env_file: ../../.env
    depends_on:
      - db

  db:
    image: postgres:13
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    env_file: ../../.env

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ../../:/app
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - web

volumes:
  postgres_data:

```

<br><br>


---
### Configure Requirements Files
---

<br>

#### Open `./requirements/development/dev.requirements.txt`:

```bash
#!/usr/bin/env bash

# Open `dev.requirements.txt` with `$EDITOR`, or your choice of editor e.g. `nano`, `vim`, `subl` etc.
"${EDITOR}" "./requirements/development/dev.requirements.txt"

```

<br>

#### Update `./requirements/development/dev.requirements.txt`:

```txt 
# ./requirements/development/dev.requirements.txt

Django>=4.2,<5.0
gunicorn
psycopg2-binary

```

#### Open `./requirements/production/prod.requirements.txt`:

```bash
#!/usr/bin/env bash

# 1. Open `prod.requirements.txt` with `$EDITOR`, or your choice of editor e.g. `nano`, `vim`, `subl` etc.
"${EDITOR}" "./requirements/production/prod.requirements.txt"

```

<br>

#### Update `./requirements/production/prod.requirements.txt`:

```txt 
# ./requirements/production/prod.requirements.txt

Django>=4.2,<5.0
gunicorn
psycopg2-binary

```

<br><br>


---
### Configure Settings Files
---

<br>

#### Open `./config/settings/base.settings.py`:

```bash
#!/usr/bin/env bash

# Open `base.settings.py` with `$EDITOR`, or your choice of editor e.g. `nano`, `vim`, `subl` etc.
"${EDITOR}" "./config/settings/base.settings.py"

```

<br>

#### Update `./config/settings/base.settings.py`:

```python
# ./config/settings/base.settings.py

from pathlib import Path
import os
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Your apps here
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'db',
        'PORT': '5432',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

```

<br>

#### Open `./config/settings/development/dev.settings.py`:

```bash
#!/usr/bin/env bash

# Open `dev.settings.py` with `$EDITOR`, or your choice of editor e.g. `nano`, `vim`, `subl` etc.
"${EDITOR}" "./config/settings/development/dev.settings.py"

```

<br>

#### Update `./config/settings/development/dev.settings.py`:

```python
# ./config/settings/development/dev.settings.py
from .base import *

DEBUG = True
ALLOWED_HOSTS = ['*']

```

<br>

#### Open `./config/settings/prod.settings.py`:

```bash
#!/usr/bin/env bash

# Open `prod.settings.py` with `$EDITOR`, or your choice of editor e.g. `nano`, `vim`, `subl` etc.
"${EDITOR}" "./config/settings/prod.settings.py"

```

<br>

#### Update `./config/settings/prod.settings.py`:

```python
# ./config/settings/prod.settings.py
from .base import *

DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com']

```

<br><br>


---
### Configure Django Config Files
---

<br>

#### Open `./config/manage.py`:

```bash
#!/usr/bin/env bash

# Open `manage.py` with `$EDITOR`, or your choice of editor e.g. `nano`, `vim`, `subl` etc.
"${EDITOR}" "./manage.py"

```

<br>

#### Update `./manage.py`:

```python
#!/usr/bin/env python
# ./manage.py
import os
import sys
from pathlib import Path


def main(): 
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.development")  # new
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    current_path = Path(__file__).parent.resolve()  # new
    sys.path.append(str(current_path / "apps"))     # new
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()

```

<br>

#### Open `./config/wsgi.py`:

```bash
#!/usr/bin/env bash

# Open `wsgi.py` with `$EDITOR`, or your choice of editor e.g. `nano`, `vim`, `subl` etc.
"${EDITOR}" "./config/wsgi.py"

```

<br>

#### Update `./config/wsgi.py`:

```python
# ./config/wsgi.py
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')

```

<br><br>

---
### Configure NGINX Config File
---

<br>

#### Open `./compose/production/nginx.conf`:

```bash
#!/usr/bin/env bash

# Open `nginx.conf` with `$EDITOR`, or your choice of editor e.g. `nano`, `vim`, `subl` etc.
"${EDITOR}" "./compose/production/nginx.conf"

```

<br>

#### Update `./compose/production/nginx.conf`:

```nginxconf
# ./compose/production/nginx.conf
server {
    listen 80;

    location / {
        proxy_pass http://web:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /app/staticfiles/;
    }

    location /media/ {
        alias /app/media/;
    }
}

```

<br><br>


---
### Ensure Project Structure
---

<br>

#### Input `tree` command to print tree-like directories structure.

```bash
#!/usr/bin/env bash

#IN
tree

#OUT
.
├── apps
├── compose
│   ├── development
│   │   └── docker-compose.dev.yaml
│   └── production
│       └── docker-compose.prod.yaml
├── config
├── docker
└── requirements
    ├── development
    │   └── requirements.dev.txt
    └── production
        └── requirements.prod.txt

10 directories, 4 files

```

<br><br>


---
### Build & Run Docker Containers
---

<br>

#### For Local Development:

```bash

docker-compose up --build

```

<br>

#### For Production:

```bash

cd compose/production
docker-compose up --build -d

```

<br><br>


---
### Setup and Manage Static and Media Files
---

<br>

#### Run collectstatic to gather static files:

```bash

docker-compose run --rm web python manage.py collectstatic

```

<br>

#### Migrate the Database:

```bash

docker-compose run --rm web python manage.py migrate

```

<br><br>

---
### Final Configuration and Customization
---

<br>
