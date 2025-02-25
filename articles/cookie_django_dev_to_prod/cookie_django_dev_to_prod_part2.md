# From Development To Production: Initializing a Scalable Cookiecutter-Django Project (Part 2 - Docker Build & Users)

<br>

![Python Zen](https://i.ibb.co/SD0gyY8n/python-zen-background.jpg)

<br>

## 🚀 Introduction

Managing users securely is essential when working with **Cookiecutter-Django**. This guide provides best practices for managing user roles, executing commands inside Docker containers, and enforcing authentication and authorization mechanisms.

---

<br>

## ⚡ Step 1: Running Docker commands with Bash Aliases

To simplify running and shutting down the project, migrations, admin commands, etc., add these aliases to your `.bashrc` or wherever you stash your alias's, usually located in `"${HOME}/.bashrc"`:

```bash
# ~/.bashrc

alias djcreatesu='docker-compose -f docker-compose.local.yml run --rm django python manage.py createsuperuser'
alias djmakemigrations='docker-compose -f docker-compose.local.yml run --rm django python manage.py makemigrations'
alias djmigrate='docker-compose -f docker-compose.local.yml run --rm django python manage.py migrate'
alias djshellplus='docker-compose -f docker-compose.local.yml run --rm django python manage.py shell_plus'

alias djbuild='docker-compose -f docker-compose.local.yml build'
alias djlogs='docker-compose -f docker-compose.local.yml logs -f --timestamps'
alias djup='docker-compose -f docker-compose.local.yml up -d --build && 
docker-compose -f docker-compose.local.yml logs -f --timestamps'
alias djrestart='docker-compose -f docker-compose.local.yml down && 
docker-compose -f docker-compose.local.yml up -d --build && 
docker-compose -f docker-compose.local.yml logs -f --timestamps'
alias djdown='docker-compose -f docker-compose.local.yml down'
```

**Django alias's**:

- **djcreatesu**: Create superuser for project. 
- **djmakemigrations**: Make database migrations.
- **djmigrate**: Migrate database.
- **djshellplus**: Jump into shell inside container.

**Docker alias's**

- **djbuild**: Build the containers.
- **djlogs**: Monitor the container logs.
- **djup**: Build the containers, run in detached mode and monitor logs.
- **djdown**: Bring down the containers.

Reload your shell:

```bash
#!/usr/bin/env bash
. "${HOME}/.bashrc"
```

Now, you can use the alias's instead of typing out the whole command every time 🚀.

---

<br>

## 🛠 Step 2: Build the Docker Containers with Docker-Compose

Start with the Cookiecutter-Django project initialized in Part 1 and build the containers locally. Ensure **Docker** and **Docker-Compose** are installed. We will use the alias from above.

```bash
#!/usr/bin/env bash

djbuild

```

This will take a while, so be patient while the containers are built. ⏳

---

<br>

## 📦 Step 3: Migrate the Database and Create a Superuser

Once the containers are built, migrate the database inside the container using:

```bash
#!/usr/bin/env bash

djmigrate

```

```txt

[+] Creating 2/2
 ✔ Container cookie_django_dev_to_prod_local_redis     Running 0.0s 
 ✔ Container cookie_django_dev_to_prod_local_postgres  Running 0.0s 
wait-for-it: waiting 30 seconds for postgres:5432
wait-for-it: postgres:5432 is available after 0 seconds
PostgreSQL is available
Operations to perform:
  Apply all migrations: account, admin, auth, contenttypes, django_celery_beat, 
  mfa, sessions, sites, socialaccount, users
Running migrations:
  No migrations to apply.

```

Then, create a superuser for admin access:

```bash
#!/usr/bin/env bash

djcreatesu

```

```txt

[+] Creating 2/2
 ✔ Container cookie_django_dev_to_prod_local_redis     Running 0.0s 
 ✔ Container cookie_django_dev_to_prod_local_postgres  Running 0.0s 
wait-for-it: waiting 30 seconds for postgres:5432
wait-for-it: postgres:5432 is available after 0 seconds
PostgreSQL is available
Email address: example@mail.com
Password: 
Password (again): 
Superuser created successfully.

```

You'll be prompted to enter an **email and password** (the password input will be hidden for security reasons).

---

<br>

## 🔧 Step 4: Initialize Pre-Commit

Before making a `git commit`, initialize `pre-commit` to install hooks:

```bash
#!/usr/bin/env bash

git init

```

```txt

Initialized empty Git repository in /.git/

```

```bash
#!/usr/bin/env bash

pre-commit install

```

```txt

pre-commit installed at .git/hooks/pre-commit

```

This ensures code quality by running checks before commits. ✅

---

<br>

## Step 5: Run the Project

Run the project using the alias from earlier:

```bash
#!/usr/bin/env bash

dup

```

You should see a bunch of output with the following towards the end:

```txt
...

cookie_django_dev_to_prod_local_django | 2025-02-23T23:41:09.639378668Z Performing system checks...
cookie_django_dev_to_prod_local_django | 2025-02-23T23:41:09.639778350Z 
cookie_django_dev_to_prod_local_django | 2025-02-23T23:41:09.808801824Z System check identified no issues (0 silenced).
cookie_django_dev_to_prod_local_django | 2025-02-23T23:41:09.907384576Z 
cookie_django_dev_to_prod_local_django | 2025-02-23T23:41:09.907404647Z Django version 5.0.12, using settings 'config.settings.local'
cookie_django_dev_to_prod_local_django | 2025-02-23T23:41:09.907406797Z Development server is running at http://0.0.0.0:8000/
cookie_django_dev_to_prod_local_django | 2025-02-23T23:41:09.907408925Z Using the Werkzeug debugger (https://werkzeug.palletsprojects.com/)
cookie_django_dev_to_prod_local_django | 2025-02-23T23:41:09.907411444Z Quit the server with CONTROL-C.
cookie_django_dev_to_prod_local_django | 2025-02-23T23:41:10.095818422Z  * Debugger is active!
cookie_django_dev_to_prod_local_django | 2025-02-23T23:41:10.096582244Z  * Debugger PIN: 633-932-422

...

```

Your Django app should now be running! 🎉

---

<br>

## 🌍 Step 6: Accessing the App in the Browser

Try accessing the app at:
- `http://localhost:8000`
- `http://127.0.0.1:8000`
- `http://172.18.0.1:8000` (my docker internal network ip)

If you encounter an **error page** or nothing loads, check the **Docker network** to find the correct internal IP:

```bash
#!/usr/bin/env bash

docker network ls

```

```txt

NETWORK ID     NAME                                DRIVER    SCOPE
693f3915c2ee   bridge                              bridge    local
10e27e367ede   cookie_django_dev_to_prod_default   bridge    local  # grab the NETWORK ID 
840d8e4172ab   host                                host      local
cee16dd5679a   none                                null      local

```

Then we will inspect the network.

```bash
#!/usr/bin/env bash

docker network inspect 10e27e367ede  # NETWORK ID

```

```txt

[
    {
        "Name": "cookie_django_dev_to_prod_default",
        "Id": "....",
        "Created": "...",
        "Scope": "local",
        "Driver": "bridge",
        "EnableIPv6": false,
        "IPAM": {
            "Driver": "default",
            "Options": null,
            "Config": [
                {
                    "Subnet": "172.18.0.0/16",
                    "Gateway": "172.18.0.1"         # the goodies
                }
            ]
        }
        ...
]

```

Now open up `config/settings/local.py` and add your project's IP to `ALLOWED_HOSTS`.

```python

# ...
# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1", "172.18.0.1"]  # noqa: S104
# ...


```

Restart the project and try again. 🔄

1. `djdown`
2. `djup`
3. visit `<NETWORK ID>:8000` in the browser.

You should see the project now.

![Cookiecutter-Django App](https://i.ibb.co/rTxz7yp/brave-screenshot-1.png)

---

<br>

## 👤 Step 7: Managing User Permissions and Groups in Django

Django assigns permissions at the **model level**, allowing users to perform **add, change, and delete** operations. You can also create **custom permissions** for advanced access control.

<br>

### 🔑 Creating Custom Permissions

Modify the **User model** and add permissions in `/cookie_django_dev_to_prod/users/models.py`:

```python

from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Meta:
        permissions = [
            ("can_post", "Can post articles."),
        ]

```

Run django makemigrations:

```bash
#!/usr/bin/env bash

djmakemigrations

```

```txt

[+] Creating 2/2
 ✔ Container cookie_django_dev_to_prod_local_redis     Running 0.0s 
 ✔ Container cookie_django_dev_to_prod_local_postgres  Running 0.0s 
wait-for-it: waiting 30 seconds for postgres:5432
wait-for-it: postgres:5432 is available after 0 seconds
PostgreSQL is available
Migrations for 'users':
  cookie_django_dev_to_prod/users/migrations/0002_alter_user_options.py
    - Change Meta options on user

```

Then, run django migrate:

```bash
#!/usr/bin/env bash

djmigrate

```

```txt

[+] Creating 2/2
 ✔ Container cookie_django_dev_to_prod_local_redis     Running 0.0s 
 ✔ Container cookie_django_dev_to_prod_local_postgres  Running 0.0s 
wait-for-it: waiting 30 seconds for postgres:5432
wait-for-it: postgres:5432 is available after 0 seconds
PostgreSQL is available
Operations to perform:
  Apply all migrations: account, admin, auth, contenttypes, django_celery_beat, 
  mfa, sessions, sites, socialaccount, users
Running migrations:
  Applying users.0002_alter_user_options... OK

```

### 🎭 Assigning Permissions to Users

Assign permissions using Django's shell_plus alias:

```bash
#!/usr/bin/env bash

djshellplus

```

```txt

[+] Creating 2/2
 ✔ Container cookie_django_dev_to_prod_local_postgres  Running 0.0s 
 ✔ Container cookie_django_dev_to_prod_local_redis     Running 0.0s 
wait-for-it: waiting 30 seconds for postgres:5432
wait-for-it: postgres:5432 is available after 0 seconds
PostgreSQL is available
# Shell Plus Model Imports
from allauth.account.models import EmailAddress, EmailConfirmation
from allauth.mfa.models import Authenticator
from allauth.socialaccount.models import SocialAccount, SocialApp, SocialToken
from cookie_django_dev_to_prod.users.models import User
from django.contrib.admin.models import LogEntry
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.sessions.models import Session
from django.contrib.sites.models import Site
from django_celery_beat.models import ClockedSchedule, CrontabSchedule, 
IntervalSchedule, PeriodicTask, PeriodicTasks, SolarSchedule
# Shell Plus Django Imports
from django.core.cache import cache
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import Avg, Case, Count, F, Max, Min, Prefetch, Q, Sum, When
from django.utils import timezone
from django.urls import reverse
from django.db.models import Exists, OuterRef, Subquery
Python 3.12.9 (main, Feb  6 2025, 22:37:05) [GCC 12.2.0]
Type 'copyright', 'credits' or 'license' for more information
IPython 8.32.0 -- An enhanced Interactive Python. Type '?' for help.

```

Inside the shell:

```python

from django.contrib.auth.models import Permission
from django.contrib.auth import get_user_model
User = get_user_model()

user = User.objects.first()
permission = Permission.objects.get(codename="can_post")
user.user_permissions.add(permission)
user.save()

```

Verify the permission:

```python

user.user_permissions.all()

```

```txt

<QuerySet [<Permission: Users | user | Can post articles.>]>

```

### 🏷 Using Groups for Role-Based Access

Groups simplify role-based permissions. Create a group and assign permissions:

```python

from django.contrib.auth.models import Group

authors = Group.objects.create(name="Authors")
permission = Permission.objects.get(codename="can_post")
authors.permissions.add(permission)
authors.save()

```

Assign a user to a group:

```python

user.groups.add(authors)

```

Check if a user belongs to a group:

```python

user.groups.filter(name="Authors").exists()

```

```txt

True

```

### 🔒 Restricting User Access in Views

Use `@permission_required` to restrict access:

```python

from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse

@permission_required("app_name.can_post", raise_exception=True)
def create_article(request):
    # ...
    return HttpResponse("Article Posted!")

```

For class-based views:

```python

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import TemplateView

class CreateArticleView(PermissionRequiredMixin, TemplateView):
    template_name = "create_article.html"
    permission_required = "articles.can_post"

```

Django's **permission system** ensures fine-grained access control, allowing secure user role management. 🔐

---

<br>

## 🎯 Conclusion

Managing users securely is critical in a **Cookiecutter-Django** project. By implementing **role-based access control (RBAC)**, we significantly reduce security risks.

Today, we:
✅ Configured project aliases for efficiency
✅ Learned how to run commands in the container
✅ Built Docker containers
✅ Managed users & permissions

---

<br>

## ⏭️ Next Up

In **Part 3**, we'll cover **sending emails using Django signals & Celery tasks**. 📩

<br>

**Enjoyed this guide? Like, share, and follow to stay updated and so I know there's interest! 🚀**

<br>

---

## Contact

[![GitHub Logo](https://i.ibb.co/tTg2pMYH/Github-logo-duotone.png)](https://github.com/neoncrypto/linkedin/blob/main/articles/cookie_django_dev_to_prod/cookie_django_dev_to_prod.md) [![LinkedIn Logo](https://i.ibb.co/4RNvKK5N/Linkedin-logo-duotone.png)](https://www.linkedin.com/in/neoncrypto0)
