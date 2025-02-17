# From Development To Production: Initializing a Scalable Cookiecutter-Django Project (Part 1 - Key Features & Benefits)

<br>

![2 Scoops Of Django Image](https://i.ibb.co/LDRd6MHC/2scoopsdjango.png)

<br>

## Introduction
Building a robust, production-ready Django application from scratch can be time-consuming and complex. However, with **Cookiecutter Django**, you get a well-structured, secure, and scalable starting point right out of the box. This guide will walk you through setting up, configuring, and deploying a **Dockerized Cookiecutter-Django project**, ensuring best practices and security along the way.

This guide will be broken down in parts and is geared towards developers who know their way around `bash` shell. By the end of this part, you'll have a working Django application with **Docker support**, and a better understanding of the benefits of using `Cookiecutter-Django`.

---

<br>

## Prerequisites
Before proceeding, make sure you have the following installed on your system:

- **Linux Environment** (with Bash and Python installed)
- **Docker** ([Installation Guide](https://docs.docker.com/install/#supported-platforms))
- **Docker-Compose** ([Installation Guide](https://docs.docker.com/compose/install/))
- **Pre-commit** ([Installation Guide](https://pre-commit.com/#install))
- **Tree (optional)** ([Installation Guide](https://www.geeksforgeeks.org/tree-command-unixlinux/))

---

<br>


## Step 1: Create a Virtual Environment and Install Cookiecutter
To ensure a clean development environment, start by creating and activating a Python virtual environment:

```bash
#!/usr/bin/env bash

python -m venv --copies --upgrade-deps env  # create environment
. "${PWD}/env/bin/activate"                 # activate environment
type python                                 # verify python is "${PWD}/env/bin/python"
type pip                                    # verify pip is "$[PWD}/env/bin/pip"
pip install cookiecutter                    # install cookiecutter in environment
type cookiecutter                           # verify cookiecutter is "${PWD}/env/bin/cookiecutter"

```

---

<br>

## Step 2: Generate a New Cookiecutter-Django Project
Run the following command to create a new project based on **Cookiecutter Django**:

```bash
#!/usr/bin/env bash

cookiecutter gh:cookiecutter/cookiecutter-django

```

You'll be prompted with a series of questions to configure your project. For this guide, you can use the following sample values, just hit enter to accept defatults if there's no value:

```txt

[1/27] project_name (My Awesome Project): Cookie Django Dev To Prod
[2/27] project_slug (cookie_django_dev_to_prod): 
[3/27] description (Behold My Awesome Project!): From Development To Production: Initializing a Scalable Cookiecutter-Django Project
[4/27] author_name (Daniel Roy Greenfeld): Change Me
[5/27] domain_name (example.com): changeme.com
[6/27] email (change-me@changeme.com): 
[7/27] version (0.1.0): 
[8/27] Select open_source_license
  1 - MIT
  2 - BSD
  3 - GPLv3
  4 - Apache Software License 2.0
  5 - Not open source
  Choose from [1/2/3/4/5] (1): 
[9/27] Select username_type
  1 - username
  2 - email
  Choose from [1/2] (1): 2
[10/27] timezone (UTC): 
[11/27] windows (n): 
[12/27] Select editor
  1 - None
  2 - PyCharm
  3 - VS Code
  Choose from [1/2/3] (1): 
[13/27] use_docker (n): y
[14/27] Select postgresql_version
  1 - 16
  2 - 15
  3 - 14
  4 - 13
  5 - 12
  Choose from [1/2/3/4/5] (1): 
[15/27] Select cloud_provider
  1 - AWS
  2 - GCP
  3 - Azure
  4 - None
  Choose from [1/2/3/4] (1): 
[16/27] Select mail_service
  1 - Mailgun
  2 - Amazon SES
  3 - Mailjet
  4 - Mandrill
  5 - Postmark
  6 - Sendgrid
  7 - Brevo
  8 - SparkPost
  9 - Other SMTP
  Choose from [1/2/3/4/5/6/7/8/9] (1): 
[17/27] use_async (n): 
[18/27] use_drf (n):  
[19/27] Select frontend_pipeline
  1 - None
  2 - Django Compressor
  3 - Gulp
  4 - Webpack
  Choose from [1/2/3/4] (1): 2
[20/27] use_celery (n): y
[21/27] use_mailpit (n): 
[22/27] use_sentry (n): 
[23/27] use_whitenoise (n): 
[24/27] use_heroku (n): 
[25/27] Select ci_tool
  1 - None
  2 - Travis
  3 - Gitlab
  4 - Github
  5 - Drone
  Choose from [1/2/3/4/5] (1): 4
[26/27] keep_local_envs_in_vcs (y): 
[27/27] debug (n): y
[SUCCESS]: Project initialized, keep up the good work!

```

Upon successful execution, your new **Cookiecutter-Django** project will be initialized.

📄 [Cookiecutter-Django Docs](https://cookiecutter-django.readthedocs.io/en/latest/1-getting-started/project-generation-options.html)

---

<br>

## Step 3: Print Project Structure
To inspect the generated directory structure, use the `tree` command:

```bash
#!/usr/bin/env bash

tree -a --dirsfirst "${PWD}/cookie_django_dev_to_prod"

```

```txt

├── compose
│   ├── local
│   │   ├── django
│   │   │   ├── celery
│   │   │   │   ├── beat
│   │   │   │   │   └── start
│   │   │   │   ├── flower
│   │   │   │   │   └── start
│   │   │   │   └── worker
│   │   │   │       └── start
│   │   │   ├── Dockerfile
│   │   │   └── start
│   │   └── docs
│   │       ├── Dockerfile
│   │       └── start
│   └── production
│       ├── aws
│       │   ├── maintenance
│       │   │   ├── download
│       │   │   └── upload
│       │   └── Dockerfile
│       ├── django
│       │   ├── celery
│       │   │   ├── beat
│       │   │   │   └── start
│       │   │   ├── flower
│       │   │   │   └── start
│       │   │   └── worker
│       │   │       └── start
│       │   ├── Dockerfile
│       │   ├── entrypoint
│       │   └── start
│       ├── postgres
│       │   ├── maintenance
│       │   │   ├── _sourced
│       │   │   │   ├── constants.sh
│       │   │   │   ├── countdown.sh
│       │   │   │   ├── messages.sh
│       │   │   │   └── yes_no.sh
│       │   │   ├── backup
│       │   │   ├── backups
│       │   │   ├── restore
│       │   │   └── rmbackup
│       │   └── Dockerfile
│       └── traefik
│           ├── Dockerfile
│           └── traefik.yml
├── config
│   ├── settings
│   │   ├── base.py
│   │   ├── __init__.py
│   │   ├── local.py
│   │   ├── production.py
│   │   └── test.py
│   ├── api_router.py
│   ├── celery_app.py
│   ├── __init__.py
│   ├── urls.py
│   └── wsgi.py
├── cookie_django_dev_to_prod
│   ├── contrib
│   │   ├── sites
│   │   │   ├── migrations
│   │   │   │   ├── 0001_initial.py
│   │   │   │   ├── 0002_alter_domain_unique.py
│   │   │   │   ├── 0003_set_site_domain_and_name.py
│   │   │   │   ├── 0004_alter_options_ordering_domain.py
│   │   │   │   └── __init__.py
│   │   │   └── __init__.py
│   │   └── __init__.py
│   ├── static
│   │   ├── css
│   │   │   └── project.css
│   │   ├── fonts
│   │   │   └── .gitkeep
│   │   ├── images
│   │   │   └── favicons
│   │   │       └── favicon.ico
│   │   └── js
│   │       └── project.js
│   ├── templates
│   │   ├── account
│   │   │   └── base_manage_password.html
│   │   ├── allauth
│   │   │   ├── elements
│   │   │   │   ├── alert.html
│   │   │   │   ├── badge.html
│   │   │   │   ├── button.html
│   │   │   │   ├── field.html
│   │   │   │   ├── fields.html
│   │   │   │   ├── panel.html
│   │   │   │   └── table.html
│   │   │   └── layouts
│   │   │       ├── entrance.html
│   │   │       └── manage.html
│   │   ├── pages
│   │   │   ├── about.html
│   │   │   └── home.html
│   │   ├── users
│   │   │   ├── user_detail.html
│   │   │   └── user_form.html
│   │   ├── 403_csrf.html
│   │   ├── 403.html
│   │   ├── 404.html
│   │   ├── 500.html
│   │   └── base.html
│   ├── users
│   │   ├── api
│   │   │   ├── __init__.py
│   │   │   ├── serializers.py
│   │   │   └── views.py
│   │   ├── migrations
│   │   │   ├── 0001_initial.py
│   │   │   └── __init__.py
│   │   ├── tests
│   │   │   ├── api
│   │   │   │   ├── __init__.py
│   │   │   │   ├── test_openapi.py
│   │   │   │   ├── test_urls.py
│   │   │   │   └── test_views.py
│   │   │   ├── factories.py
│   │   │   ├── __init__.py
│   │   │   ├── test_admin.py
│   │   │   ├── test_forms.py
│   │   │   ├── test_managers.py
│   │   │   ├── test_models.py
│   │   │   ├── test_tasks.py
│   │   │   ├── test_urls.py
│   │   │   └── test_views.py
│   │   ├── adapters.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── context_processors.py
│   │   ├── forms.py
│   │   ├── __init__.py
│   │   ├── managers.py
│   │   ├── models.py
│   │   ├── tasks.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── conftest.py
│   └── __init__.py
├── .devcontainer
│   ├── bash_history
│   ├── bashrc.override.sh
│   └── devcontainer.json
├── docs
│   ├── conf.py
│   ├── howto.rst
│   ├── index.rst
│   ├── __init__.py
│   ├── make.bat
│   ├── Makefile
│   └── users.rst
├── .envs
│   ├── .local
│   │   ├── .django
│   │   └── .postgres
│   └── .production
│       ├── .django
│       └── .postgres
├── .github
│   ├── workflows
│   │   └── ci.yml
│   └── dependabot.yml
├── locale
│   ├── en_US
│   │   └── LC_MESSAGES
│   │       └── django.po
│   ├── fr_FR
│   │   └── LC_MESSAGES
│   │       └── django.po
│   ├── pt_BR
│   │   └── LC_MESSAGES
│   │       └── django.po
│   └── README.md
├── requirements
│   ├── base.txt
│   ├── local.txt
│   └── production.txt
├── tests
│   ├── __init__.py
│   └── test_merge_production_dotenvs_in_dotenv.py
├── CONTRIBUTORS.txt
├── docker-compose.docs.yml
├── docker-compose.local.yml
├── docker-compose.production.yml
├── .dockerignore
├── .editorconfig
├── .gitattributes
├── .gitignore
├── justfile
├── LICENSE
├── manage.py
├── merge_production_dotenvs_in_dotenv.py
├── .pre-commit-config.yaml
├── pyproject.toml
├── .python-version
├── README.md
└── .readthedocs.yml
61 directories, 140 files

```

Don't be overwhelmed. The generated structure is well-organized, ready to use with only a few configurations, and follows Django best practices, including **secure settings**, **modular configurations**, and **Docker integration**.

📄 [Tree Docs](https://linux.die.net/man/1/tree)

---

<br>

## Key Features & Benefits
### 1. Secure Settings Configuration
Managing sensitive information securely is crucial in any production application. Cookiecutter Django leverages **django-environ** to store configuration settings in environment variables rather than hardcoding them into the project files. This practice minimizes the risk of exposing credentials and enhances the portability of your application.

✅ **Prevents credential leaks** by avoiding hardcoded sensitive information. <br>
✅ **Improves security** by keeping environment-specific configurations separate. <br>
✅ **Simplifies deployment** by allowing easy environment variable management.

**Environment variables** &nbsp; 👉 `/cookie_django_dev_to_prod/.envs` <br>

📄 [Django-Environ Docs](https://github.com/joke2k/django-environ)

<br>

### 2. SSL and HTTPS Enforcement
By default, Cookiecutter Django enables SSL enforcement by setting `SECURE_SSL_REDIRECT = True` in production settings. This forces all HTTP requests to be redirected to HTTPS, ensuring data transmitted between clients and the server remains encrypted and protected from man-in-the-middle attacks.

✅ **Enhances security** by encrypting all data in transit. <br>
✅ **Meets compliance requirements** for handling sensitive user information. <br>
✅ **Boosts SEO rankings** since search engines favor HTTPS-secured sites.

**Configuration file** &nbsp; 👉 `/cookie_django_dev_to_prod/config/settings/production.py` <br>

📄 [Django Docs](https://docs.djangoproject.com/en/stable/ref/settings/#secure-ssl-redirect)

<br>

### 3. Content Security Policies
Cookiecutter Django includes security settings such as `SECURE_CONTENT_TYPE_NOSNIFF` and `SECURE_FRAME_DENY` to safeguard against various web vulnerabilities:

- **Clickjacking Protection:** `SECURE_FRAME_DENY = True` prevents your site from being embedded in an iframe by malicious actors.
- **MIME Sniffing Prevention:** `SECURE_CONTENT_TYPE_NOSNIFF = True` ensures browsers do not attempt to interpret files as different MIME types.

✅ **Reduces risks of cross-site scripting (XSS) attacks.** <br>
✅ **Enhances security by enforcing strict content handling policies.**

**Configuration file** &nbsp; 👉 `/cookie_django_dev_to_prod/config/settings/production.py`

📄 [Django Docs](https://docs.djangoproject.com/en/stable/ref/settings/)

<br>

### 4. User Authentication with Allauth
Cookiecutter Django integrates **django-allauth**, providing a robust authentication system out-of-the-box. Features include:

- **Email-based authentication** (instead of usernames).
- **Social authentication** (Google, Facebook, GitHub, etc.).
- **Multi-factor authentication** options.

✅ **Secure user registration and authentication workflows.** <br>
✅ **Easily customizable login flows and social authentication providers.** <br>
✅ **Built-in password reset functionality.**

**User management files** &nbsp; 👉 `/cookie_django_dev_to_prod/cookie_django_dev_to_prod/users`

📄 [Allauth Docs](https://django-allauth.readthedocs.io/en/latest/)

<br>

### 5. Admin Panel Security
Django’s default admin panel is a common target for brute force attacks. Cookiecutter Django adds an extra layer of security by requiring a randomly generated **admin URL**, set in an environment variable (`DJANGO_ADMIN_URL`).


```bash
#!/usr/bin/env bash

python -c 'import uuid;print(uuid.uuid4().hex);'

664523d9906944a7b8c12b1dfc4a57d4

```

Then add the generated key to `/cookie_django_dev_to_prod/.envs/.production/.django`:

```txt

# add the ending '/'
DJANGO_ADMIN_URL=664523d9906944a7b8c12b1dfc4a57d4/

```

✅ **Reduces brute-force attack risks by obscuring the admin URL.** <br>
✅ **Ensures access is restricted to authorized users.**

**Secure admin settings in** &nbsp; 👉 `/cookie_django_dev_to_prod/.envs/.production/.django`

<br>

### 6. Static & Media File Management
Handling static and media files efficiently is crucial for performance and scalability. Cookiecutter Django integrates with **Amazon S3, Google Cloud Storage, and Azure Storage**, ensuring:

✅ **High availability** of static files globally. <br>
✅ **Reduced server load** by offloading media and static file hosting. <br>
✅ **Scalability** for handling large assets efficiently.

**Static files location** &nbsp; 👉 `/cookie_django_dev_to_prod/cookie_django_dev_to_prod/static` <br>
📄 [Amazon S3](https://aws.amazon.com/s3/) <br>
📄 [Google Cloud Storage](https://cloud.google.com/storage) <br>
📄 [Azure Storage](https://azure.microsoft.com/en-us/products/storage/)

<br>

### 7. Managed Database Integration
Cookiecutter Django makes it easy to integrate with managed database services such as **DigitalOcean Managed Databases, AWS RDS, and Google Cloud SQL**, using environment variables to configure database connections securely.

✅ **Automated backups** and failover protection. <br>
✅ **Scalability** with managed services handling load balancing and high availability. <br>
✅ **Security** with encrypted connections and IAM-based authentication.

**Database configuration files:**
👉 `/cookie_django_dev_to_prod/compose/production/django/entrypoint`
👉 `/cookie_django_dev_to_prod/.envs/.production/.postgres`

📄 [DigitalOcean Managed Databases](https://www.digitalocean.com/products/managed-databases) <br>
📄 [AWS RDS](https://aws.amazon.com/rds/) <br>
📄 [Google Cloud SQL](https://cloud.google.com/sql)

<br>

### 8. Task Scheduling with Celery and Celery Beat
Cookiecutter Django includes **Celery** for asynchronous task execution and **Celery Beat** for periodic task scheduling. These tools allow for background task execution, such as:

- **Sending emails** asynchronously to avoid blocking user interactions.
- **Generating reports and processing large datasets.**
- **Scheduling recurring jobs, such as clearing expired sessions.**

✅ **Improves application responsiveness by delegating long-running tasks.** <br>
✅ **Automates recurring background processes efficiently.**

📄 [Celery Docs](https://docs.celeryq.dev/en/stable/index.html) <br>
📄 [Django Celery Beat Docs](https://django-celery-beat.readthedocs.io/en/latest/)

---

<br>

## Next Up

In **Part 2** we may:

- Expand further on this article.
- Build the **Docker containers**.
- Learn how to run commands inside the **Docker container**.
- Set up **user authentication**.
- Learn how to properly create **new Django apps**.
- Add [DjangoRestFramework](https://www.django-rest-framework.org/) for API endpoints.
- ... ?

Let me know if you have a preference on what to cover!

<br>

**If you found this guide helpful, like, share, and/or follow so I know there's interest!**

---

<br>

## Bonus
Dont just learn it -[Grok It!](https://www.grokcode.com/95/definition-and-origin-of-grok/)
> When you claim to `grok` some knowledge or technique, you are asserting that 
> you have not merely learned it in a detached instrumental way but that it has 
> become part of you, part of your identity. For example, to say that you “know” 
> LISP is simply to assert that you can code in it if necessary — but to say you 
> `grok` LISP is to claim that you have deeply entered the world-view and spirit 
> of the language, with the implication that it has transformed your view of 
> programming. Contrast zen, which is similar supernal understanding experienced 
> as a single brief flash.

<br>

---

## Contact

[![GitHub Logo](https://i.ibb.co/tTg2pMYH/Github-logo-duotone.png)](https://github.com/neoncrypto/linkedin/blob/main/articles/cookie_django_dev_to_prod/cookie_django_dev_to_prod.md) [![LinkedIn Logo](https://i.ibb.co/4RNvKK5N/Linkedin-logo-duotone.png)](https://www.linkedin.com/in/neoncrypto0)
