# From Development to Production: Initializing a Scalable Cookiecutter-Django Project (Part 3 - Celery & Email)

<br>

![Django Celery](https://i.ibb.co/zVRgQqG2/docker-django-celery-redis.png)

<br>

## 📧 Introduction

Email notifications play a crucial role in modern web applications, ensuring users receive timely updates regarding their accounts, transactions, and other critical system activities. Whether sending **welcome emails**, **password reset instructions**, or **order confirmations**, managing emails efficiently enhances user experience and maintains application reliability.

In this guide, we will integrate **email notifications** into our **Cookiecutter-Django** project using **Django signals** and **Celery tasks**. These tools allow emails to be processed **asynchronously**, ensuring smooth and uninterrupted user interactions. Additionally, we will explore **Celery Beat** to schedule automated periodic tasks such as **daily reports, reminders, and system notifications**. By the end of this guide, you will be able to configure Django to send **welcome emails** and **scheduled newsletters** using Celery and Celery Beat while monitoring tasks with Celery Flower.

---

<br>


## 🚀 Step 1: Celery's Security and Performance Settings

Cookiecutter-Django comes with **pre-configured Celery settings**, providing a robust foundation for secure and efficient task execution:

```python

# Celery
# ------------------------------------------------------------------------------
if USE_TZ:
    # https://docs.celeryq.dev/en/stable/userguide/configuration.html#std:setting-timezone
    CELERY_TIMEZONE = TIME_ZONE

# https://docs.celeryq.dev/en/stable/userguide/configuration.html#std:setting-broker_url
CELERY_BROKER_URL = REDIS_URL

# https://docs.celeryq.dev/en/stable/userguide/configuration.html#redis-backend-use-ssl
CELERY_BROKER_USE_SSL = {"ssl_cert_reqs": ssl.CERT_NONE} if REDIS_SSL else None

# https://docs.celeryq.dev/en/stable/userguide/configuration.html#std:setting-result_backend
CELERY_RESULT_BACKEND = REDIS_URL

# https://docs.celeryq.dev/en/stable/userguide/configuration.html#redis-backend-use-ssl
CELERY_REDIS_BACKEND_USE_SSL = CELERY_BROKER_USE_SSL

# https://docs.celeryq.dev/en/stable/userguide/configuration.html#result-extended
CELERY_RESULT_EXTENDED = True  # Stores additional metadata about task results

# https://docs.celeryq.dev/en/stable/userguide/configuration.html#result-backend-always-retry
CELERY_RESULT_BACKEND_ALWAYS_RETRY = True  # Retries backend connection issues

# https://docs.celeryq.dev/en/stable/userguide/configuration.html#result-backend-max-retries
CELERY_RESULT_BACKEND_MAX_RETRIES = 10  # Limits retry attempts to prevent endless loops

# https://docs.celeryq.dev/en/stable/userguide/configuration.html#std:setting-accept_content
CELERY_ACCEPT_CONTENT = ["json"]

# https://docs.celeryq.dev/en/stable/userguide/configuration.html#std:setting-task_serializer
CELERY_TASK_SERIALIZER = "json"

# https://docs.celeryq.dev/en/stable/userguide/configuration.html#std:setting-result_serializer
CELERY_RESULT_SERIALIZER = "json"

# https://docs.celeryq.dev/en/stable/userguide/configuration.html#task-time-limit
CELERY_TASK_TIME_LIMIT = 5 * 60  # Prevents tasks from running indefinitely

# https://docs.celeryq.dev/en/stable/userguide/configuration.html#task-soft-time-limit
CELERY_TASK_SOFT_TIME_LIMIT = 60  # Allows graceful termination before the hard limit

# https://docs.celeryq.dev/en/stable/userguide/configuration.html#beat-scheduler
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"

# https://docs.celeryq.dev/en/stable/userguide/configuration.html#worker-send-task-events
CELERY_WORKER_SEND_TASK_EVENTS = True  # Enables monitoring of Celery tasks

# https://docs.celeryq.dev/en/stable/userguide/configuration.html#std-setting-task_send_sent_event
CELERY_TASK_SEND_SENT_EVENT = True  # Sends an event when a task is dispatched

# https://docs.celeryq.dev/en/stable/userguide/configuration.html#worker-hijack-root-logger
CELERY_WORKER_HIJACK_ROOT_LOGGER = False  # Prevents Celery from interfering with Django logging

```

### 🔐 Key Security Settings

1. **`CELERY_BROKER_USE_SSL`** & **`CELERY_REDIS_BACKEND_USE_SSL`**
   - Encrypts communication between Celery and Redis, preventing unauthorized access and data interception.
   - If `REDIS_SSL` is enabled, SSL enforcement secures all message transactions.

2. **`CELERY_ACCEPT_CONTENT`**, **`CELERY_TASK_SERIALIZER`**, and **`CELERY_RESULT_SERIALIZER`**
   - Restricts serialization formats to **JSON** to prevent security vulnerabilities associated with Pickle-based deserialization attacks.
   - Ensures that Celery workers process only safe, human-readable data.

### ⚡ Performance & Reliability Settings

1. **`CELERY_TASK_TIME_LIMIT`** & **`CELERY_TASK_SOFT_TIME_LIMIT`**
   - The **soft time limit (60 seconds)** gives tasks a chance to gracefully complete before the **hard limit (5 minutes)** is enforced.
   - Prevents runaway tasks from consuming excessive resources.

2. **`CELERY_RESULT_BACKEND_ALWAYS_RETRY`** & **`CELERY_RESULT_BACKEND_MAX_RETRIES`**
   - Automatically retries tasks if the result backend fails, preventing data loss due to temporary connection issues.
   - Limits retries to **10 attempts**, avoiding infinite retry loops.

3. **`CELERY_WORKER_HIJACK_ROOT_LOGGER = False`**
   - Keeps Celery logs separate from Django logs, ensuring clean and structured log output.

<br>

By leveraging these settings, Celery remains **secure**, **reliable**, and **efficient** for managing background task execution in production environments.

👉 `config/settings/base.py` <br>
📄 [Celery](https://docs.celeryq.dev/en/stable/userguide/configuration.html)

---

<br>


## 🔍 Step 2: Monitoring Celery with Flower

Cookiecutter-Django includes **Celery Flower**, a real-time monitoring tool for Celery workers. Flower provides insights into **task execution, worker status, and queue performance** via a web-based dashboard.

### Viewing the Flower Dashboard

Let's bring up the containers using the `dup` alias from Part 2, which should also start `flower`:

```bash
#!/usr/bin/env bash

dup  # docker-compose -f docker-compose.local.yml up -d --build     && 
     # docker-compose -f docker-compose.local.yml logs -f --timestamps

```

Once running, access the Flower dashboard on port `5555` at the `<NETWORK ID>` discovered in Part 2 of this series:

```txt

http://<NETWORK ID>:5555

Examples:
--> http://localhost:5555
--> http://172.0.0.1:5555
--> http://172.18.0.1:5555

```

![Flower Dashboard](https://i.ibb.co/svWJ3txC/brave-screenshot-2.png)

![Flower Dashboard](https://i.ibb.co/jPPcckp1/brave-screenshot-3.png)

### Features of Flower

- View active, scheduled, and completed tasks.
- Monitor worker performance and system load.
- Retry failed tasks directly from the UI.
- Inspect task execution times and queue statistics.
- Identify and debug slow or failing tasks in real-time.

Flower provides **real-time visibility and control** over Celery's task execution, making debugging and performance tuning far more efficient.

👉 `cookie_django_dev_to_prod/.envs/.local/.django` <br>
👉 `cookie_django_dev_to_prod/.envs/.production/.django` <br>
📄 [Flower](https://flower.readthedocs.io/en/latest/index.html)

---

<br>


## 📧 Step 3: Sending Mail in Cookiecutter-Django

Let's go over some of the `django` built-in functions designed to simplify sending mail programmatically.

### From Email

Let's configure the django setting `DEFAULT_FROM_EMAIL`.

Open up `config/settings/local.py`:

```bash
#!/usr/bin/env bash

nano config/settings/local.py

```

Paste in the following code at the bottom:

```python

...

DEFAULT_FROM_EMAIL = env(
    "DJANGO_DEFAULT_FROM_EMAIL",
    default="Cookie Django Dev To Prod <noreply@changeme.com>",
)

```

💾 Save and close the file (`CTRL`+`x` ➡ `y` ➡ `ENTER`)

Now, open up `.envs/.local/.django`:

```bash
#!/usr/bin/env bash

nano cookie_django_dev_to_prod/.envs/.local/.django

```

Add the following code:

```txt

...
DJANGO_DEFAULT_FROM_EMAIL=testing@testing.com

```

💾 Save and close the file (`CTRL`+`x` ➡ `y` ➡ `ENTER`)

You can repeat the same process for production or put the setting in `base.py` to make it universally available.

Now, whenever we send an email we can use `settings.DJANGO_DEFAULT_FROM_EMAIL` as the `from` email.

👉 `.envs/.local/.django` <br>
📄 [DEFAULT_FROM_EMAIL](https://docs.djangoproject.com/en/5.1/ref/settings/#default-from-email)


### Django `send_mail`

Let's jump into the `ipython` shell using the `djshellplus` alias we created in Part 2:

```bash
#!/usr/bin/env bash

djshellplus  # docker-compose -f docker-compose.local.yml run --rm django python manage.py shell_plus

```

```python

[+] Creating 2/2
✔ Container cookie_django_dev_to_prod_local_redis     Running 0.0s 
✔ Container cookie_django_dev_to_prod_local_postgres  Running 0.0s 
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
from django_celery_beat.models import ClockedSchedule, CrontabSchedule, IntervalSchedule, 
PeriodicTask, PeriodicTasks, SolarSchedule
# Shell Plus Django Imports
from django.core.cache import cache
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import Avg, Case, Count, F, Max, Min, Prefetch, Q, Sum, When
from django.utils import timezone
from django.urls import reverse
from django.db.models import Exists, OuterRef, Subquery
Python 3.12.9 (main, Feb 25 2025, 02:40:13) [GCC 12.2.0]
Type 'copyright', 'credits' or 'license' for more information
IPython 8.32.0 -- An enhanced Interactive Python. Type '?' for help.

In [1]: 

```

Now that we are inside the interactive Python shell, let's test out `django` `send_mail` and use `DJANGO_DEFAULT_FROM_EMAIL` while we're at it:

```python
#!/usr/bin/evn python
from django.conf import settings
from django.core.mail import send_mail

subject = 'Welcome To The Platform'
message = "Hello and thank you for registering! We're excited to have you."
sender = settings.DEFAULT_FROM_EMAIL
to = 'example@example.com'
send_mail(subject, message, sender, [to])

```

```txt

Content-Type: text/plain; charset="utf-8"
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit
Subject: Welcome To The Platform
From: testing@testing.com
To: example@example.com
Date: Mon, 05 Nov 1984 04:20:00 -0000
Message-ID: <174079130024.1.12425156307445650134@6ebec8b9935b>

Hello and thank you for registering! We're excited to have you.
-------------------------------------------------------------------------------

```

The emails just print to the terminal for testing purposes but show you what you're working with. We will setup real email functionality later in this series.

Exit the shell:

```python
#!/usr/bin/env python

exit

```

`send_mail` makes it easy to send plain text **AND/OR** html/text multi-part emails. To send an HTML email that also includes a text version of the email  let's first create and edit a new HTML template:

```bash
#!/usr/bin/env bash

template_dir='cookie_django_dev_to_prod/templates/users/emails'
template="${template_dir}/new_user_welcome_email.html"
mkdir "${template_dir}"  # create emails folder
touch "${template}"
nano "${template}"

```

Add this HTML code:

```html
<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Welcome Email</title>
    </head>
    <body style="font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f4f4f4;">
        <div style="max-width: 600px; margin: 20px auto; background: #ffffff; padding: 20px; border-radius: 8px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);">
            <div style="background: #0073e6; color: white; text-align: center; padding: 10px 0; font-size: 20px; font-weight: bold;">
                Welcome To The Platform {{ email }}!
            </div>
            <div style="padding: 20px; text-align: left; color: #333;">
                <p>Hello new user,</p>
                <p>Thank you for signing up for the platform {{ email }}. We’re excited to have you on board.</p>
                <p>Best regards,</p>
                <p>The Team</p>
            </div>
        </div>
    </body>
</html>

```

💾 Save and close the file (`CTRL`+`x` ➡ `y` ➡ `ENTER`)

Django's `render_to_string` method replaces all the `{{ email }}` parts with the values that we pass into the function. 

Let's see it in action, jump back in to `shell_plus`: 

```bash
#!/usr/bin/env bash

djshellplus  # docker-compose -f docker-compose.local.yml run --rm django python manage.py shell_plus

```

```python
#!/usr/bin/evn python
from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

User = get_user_model()

user = User.objects.first()  # get first user for testing
to = user.email
from_email = settings.DEFAULT_FROM_EMAIL
subject = 'Welcome To The Platform'

html_message = render_to_string(
    'users/emails/new_user_welcome_email.html', {'email': user.email }  # the magic
)
plain_message = strip_tags(html_message)  # plain text version of message.

send_mail(subject, plain_message, from_email, [to], html_message=html_message)

```

```txt

Content-Type: multipart/alternative;
 boundary="===============1668254091500648291=="
MIME-Version: 1.0
Subject: Welcome To The Platform
From: testing@testing.com
To: example@mail.com
Date: Mon, 05 Nov 1984 04:20:00 -0000
Message-ID: <174171098659.1.12520527101284414399@f0abfe16afe3>

--===============1668254091500648291==
Content-Type: text/plain; charset="utf-8"
MIME-Version: 1.0
Content-Transfer-Encoding: 8bit

Welcome Email
    
Welcome To The Platform example@mail.com!
            
Hello new user,
Thank you for signing up for the platform example@mail.com. We’re excited to have you on board.
Best regards,
The Team

--===============1668254091500648291==
Content-Type: text/html; charset="utf-8"
MIME-Version: 1.0
Content-Transfer-Encoding: 8bit

<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Welcome Email</title>
    </head>
    <body style="font-family: Arial, sans-serif;margin: 0;padding: 0;background-color: #f4f4f4;">
        <div style="max-width: 600px;margin: 20px auto;background: #ffffff;padding: 20px;border-radius: 8px;box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);">
            <div style="background: #0073e6;color: white;text-align: center;padding: 10px 0;font-size: 20px;font-weight: bold;">
                Welcome To The Platform example@mail.com!
            </div>
            <div style="padding: 20px;text-align: left;color: #333;">
                <p>Hello new user,</p>
                <p>Thank you for signing up for the platform example@mail.com. We’re excited to have you on board.</p>
                <p>Best regards,</p>
                <p>The Team</p>
            </div>
        </div>
    </body>
</html>

--===============1668254091500648291==--

```

As you can see, we are sending a single email with both a plain text and html versions of the email included in one.

Go ahead and exit the shell:

```python
#!/usr/bin/env python

exit

```

👉 `cookie_django_dev_to_prod/templates/users/emails/new_user_welcome_email.html` <br>
📄 [render_to_string](https://docs.djangoproject.com/en/5.1/topics/templates/#django.template.loader.render_to_string) <br>
📄 [strip_tags](https://docs.djangoproject.com/en/5.1/ref/utils/#django.utils.html.strip_tags) <br>
📄 [send_mail](https://docs.djangoproject.com/en/5.1/topics/templates/#django.template.loader.render_to_string)

---

<br>


## 📩 Step 4: Create Celery Task for Sending Emails using Django Signals


### Celery `shared_task`

Let's create a task that will send a HTML email on every new `User` signup.

Open `cookie_django_dev_to_prod/users/tasks.py`

```bash
#!/usr/bin/env bash
 
nano cookie_django_dev_to_prod/users/tasks.py

```

Add the following:

```python

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


@shared_task
def send_welcome_email(email):
    to = email
    from_email = settings.DEFAULT_FROM_EMAIL
    subject = 'Welcome To The Platform'
    html_message = render_to_string('users/new_user_welcome_email.html', {'email': to })
    plain_message = strip_tags(html_message)
    send_mail(subject, plain_message, from_email, [to], html_message=html_message)

```

💾 Save and close the file (`CTRL`+`x` ➡ `y` ➡ `ENTER`)

Now we can call this task automatically using Django signals or programmatically any other way we can come up with.


### Django Signals

Django **signals** provide a built-in mechanism to execute code when certain events occur in the system. We will leverage them to send **welcome emails** when a user registers using the `send_welcome_email` task function from above.

Create and open up `cookie_django_dev_to_prod/users/signals.py`:

```bash
#!/usr/bin/env bash

template='cookie_django_dev_to_prod/users/signals.py'
touch "${template}"
nano "${template}"

```

Add the following code:

```python

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from users.tasks import send_welcome_email

User = get_user_model()

@receiver(post_save, sender=User)
def send_welcome_email_signal(sender, instance, created, **kwargs):
    if created:
        send_welcome_email.delay(instance.email)

```

💾 Save and close the file (CTRL+x ➡ y ➡ ENTER)

Now using the `post_save` signal from Django, every user will receive a welcome email automatically when signing up.

👉 `cookie_django_dev_to_prod/users/signals.py` <br>
📄 [shared_task](https://docs.celeryq.dev/en/stable/django/first-steps-with-django.html#using-the-shared-task-decorator) <br>
📄 [signals](https://docs.djangoproject.com/en/5.1/topics/signals/#module-django.dispatch) <br>
📄 [post_save](https://docs.djangoproject.com/en/5.1/ref/signals/#post-save)

---

<br>


## 📅 Step 5: Scheduling a Recurring Newsletter with Celery Beat

Django-Celery-Beat allows you to schedule tasks at specific intervals. In this step, we will create a periodic task that sends a **newsletter** using a pre-defined email template.

### Create HTML Email Template for Newsletters

Create and open up `cookie_django_dev_to_prod/templates/users/emails/newsletter.html`:

```bash
#!/usr/bin/env bash

template='cookie_django_dev_to_prod/templates/users/emails/newsletter.html'
touch "${template}"
nano "${template}"

```

Add the following code:

```html

<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Newsletter Email</title>
    </head>
    <body style="font-family: Arial, sans-serif;margin: 0;padding: 0;background-color: #f4f4f4;">
        <div style="max-width: 600px;margin: 20px auto;background: #ffffff;padding: 20px;border-radius: 8px;box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);">
            <div style="background: #0073e6;color: white;text-align: center;padding: 10px 0;font-size: 20px;font-weight: bold;">
                Bi-Weekly Newsletter for {{ email }}!
            </div>
            <div style="padding: 20px;text-align: left;color: #333;">
                <p>Thank you for signing up for the newsletter {{ email }}!</p>
            </div>
        </div>
    </body>
</html>

```

💾 Save and close the file (`CTRL`+`x` ➡ `y` ➡ `ENTER`)


### Creating the Newsletter Task

Open up `cookie_django_dev_to_prod/users/tasks.py`

```bash
#!/usr/bin/env bash

nano cookie_django_dev_to_prod/users/tasks.py

```

Add the following code:

```python

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

User = get_user_model()


@shared_task
def send_newsletter():
    '''Send newsletter email to all users (DONT)'''
    users = User.objects.all()
    for user in users:
        to = user.email
        from_email = settings.DEFAULT_FROM_EMAIL
        subject = 'Bi-Weekly Newsletter'
        html_message = render_to_string('users/emails/newsletter.html', {'email': [to]})
        plain_message = strip_tags(html_message)
        send_mail(subject, plain_message, from_email, [to], html_message=html_message)

```

Note: you probably want functionality that checks for `user.subscribed` or something similar instead of sending emails to every user in production, this task is really just for demonstration.

💾 Save and close the file (`CTRL`+`x` ➡ `y` ➡ `ENTER`)


### Configuring Celery Beat

Open up `config/settings/local.py`

```bash
#!/usr/bin/env bash

nano config/settings/local.py

```

Add this code to the bottom:

```python

# https://docs.celeryq.dev/en/stable/userguide/periodic-tasks.html
CELERY_BEAT_SCHEDULE = {
    "bi_weekly_newsletter": {
        "task": "cookie_django_dev_to_prod.users.tasks.send_newsletter",
        "schedule": 30.0,                   # Every 30 seconds for testing
        # "schedule": 14 * 24 * 60 * 60,    # Every two weeks for production
    },
}

```

💾 Save and close the file (`CTRL`+`x` ➡ `y` ➡ `ENTER`)

Restart the containers with the `djrestart` alias from Part 2:

```bash
#!/usr/bin/env bash

djrestart
# docker-compose -f docker-compose.local.yml down               && 
# docker-compose -f docker-compose.local.yml up -d --build      && 
# docker-compose -f docker-compose.local.yml logs -f --timestamps'

```

You should have a `superuser` created from earlier, if not make sure to run the `djcreatesu` alias from Part 2 and create a `User`, (`docker-compose -f docker-compose.local.yml run --rm django python manage.py createsuperuser`):

Now, after a short wait you can view the logs for confirmation that the task works as expected:

```txt

INFO beat 23 139943934090112 Scheduler: Sending due task bi_weekly_newsletter (cookie_django_dev_to_prod.users.tasks.send_newsletter)
INFO strategy 32 139583013825408 Task cookie_django_dev_to_prod.users.tasks.send_newsletter[4d187e21-46d9-448a-8771-1f493dd7e7aa] received
Content-Type: multipart/alternative;
 boundary="===============7651893232125371423=="
MIME-Version: 1.0
Subject: Bi-Weekly Newsletter
From: testing@testing.com
To: ['subscriber@example.com']
Date: Mon, 05 Nov 1984 04:20:00 -0000
Message-ID: <174076777371.36.10152070327388197819@d837171afac8>

--===============7651893232125371423==
Content-Type: text/plain; charset="utf-8"
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit
        
Newsletter Email
            
Bi-Weekly Newsletter for subscriber@example.com!

Thank you for signing up for the newsletter subscriber@example.com!

--===============7651893232125371423==
Content-Type: text/html; charset="utf-8"
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit

<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Newsletter Email</title>
    </head>
    <body style="font-family: Arial, sans-serif;margin: 0;padding: 0;background-color: #f4f4f4;">
        <div style="max-width: 600px;margin: 20px auto;background: #ffffff;padding: 20px;border-radius: 8px;box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);">
            <div style="background: #0073e6;color: white;text-align: center;padding: 10px 0;font-size: 20px;font-weight: bold;">
                Bi-Weekly Newsletter for subscriber@example.com!
            </div>
            <div style="padding: 20px;text-align: left;color: #333;">
                <p>Thank you for signing up for the newsletter subscriber@example.com!</p>
            </div>
        </div>
    </body>
</html>

--===============7651893232125371423==--

-------------------------------------------------------------------------------
INFO trace 36 139583013825408 Task cookie_django_dev_to_prod.users.tasks.send_newsletter[4d187e21-46d9-448a-8771-1f493dd7e7aa] succeeded in 0.00456888199551031s: None

```

👉 `cookie_django_dev_to_prod/templates/users/emails/newsletter.html` <br>
👉 `cookie_django_dev_to_prod/users/tasks.py` <br>
👉 `config/settings/local.py` <br>
📄 [django-celery-beat](https://django-celery-beat.readthedocs.io/en/latest/)

---

<br>


## 🎯 Conclusion

In this guide, we successfully integrated **Django signals** with **Celery tasks** to enable **asynchronous email notifications**. We also explored **Celery Beat** for automating scheduled tasks and introduced **Celery Flower** for real-time monitoring. This setup allows Django applications to handle real-time and scheduled emails efficiently, improving performance and user experience.

By implementing these practices, we ensure that our Django project remains **scalable, responsive, and secure** while handling email-related workflows.

---

<br>


## ⏭️ Next Up

In Part 4, we will walk through the proper way to set up a new Cookiecutter-Django app and begin building a real-world example application from scratch.

<br>

### Enjoyed this guide?

**Like**, **share**, and **follow** to stay **updated** and so I know there's interest! 🚀

---

<br>


## Contact

[![GitHub Logo](https://i.ibb.co/tTg2pMYH/Github-logo-duotone.png)](https://github.com/neoncrypto/linkedin/blob/main/articles/cookie_django_dev_to_prod/cookie_django_dev_to_prod.md) [![LinkedIn Logo](https://i.ibb.co/4RNvKK5N/Linkedin-logo-duotone.png)](https://www.linkedin.com/in/neoncrypto0)

<br>
<br>
