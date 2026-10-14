# windwardapps.com

Django 5.2 site for Windward Apps. One Django app (`app`), one settings module,
SQLite, hCaptcha on the contact form, and a Mailgun-style HTTP API for email.

## Layout

```
manage.py            Django entry point (defaults to project.settings)
project/             settings.py, urls.py, wsgi.py
app/                 the whole site: models, views, forms, templates, static
  templates/app/     page templates; news/ for the blog, email/ for emails
  static/app/        site.css, images, jQuery + ajaxForm.js
requirements.txt     pinned dependencies
deploy.sh            rsync + restart on the production host
.env                 local environment variables (not committed)
```

## Run locally

```sh
python3 -m venv .venv                # Python 3.12 or newer
.venv/bin/pip install -r requirements.txt
.venv/bin/python manage.py migrate
.venv/bin/python manage.py runserver
```

Open http://127.0.0.1:8000/. Settings are read from the environment, and a
`.env` file at the repo root is loaded automatically. For local work you only
need `DEBUG=1`; everything else has a safe default. When no email API is
configured, outgoing mail is logged instead of sent.

```sh
.venv/bin/python manage.py test              # run the test suite
.venv/bin/python manage.py createsuperuser   # account for /admin and /login
```

## Configuration

| Variable | Purpose |
| --- | --- |
| `DEBUG` | `1` for local development. Off by default. |
| `WA_SECRET_KEY` | Required when `DEBUG` is off. |
| `ALLOWED_HOSTS` | Comma separated. Defaults to `windwardapps.com,www.windwardapps.com`. |
| `STATIC_ROOT` | Where `collectstatic` writes. Defaults to `./static`. |
| `LOG_FILE` | Production log file. Defaults to `./windwardapps.log`. |
| `WA_CONTACT_EMAIL` | Recipient of contact-form messages. |
| `WA_EMAIL_API_URL`, `WA_EMAIL_API_KEY` | Email API endpoint and key. |
| `CAPTCHA_KEY`, `CAPTCHA_SECRET` | hCaptcha site key and secret. |
| `CAPTCHA_ENFORCE` | `1` to reject contact submissions that fail the captcha. Off by default. |

## Deploy

```sh
./deploy.sh
```

Pushes `master` to GitHub, then on the `wwa` host (`/var/www/windwardapps.com`)
pulls, installs requirements into `env/`, migrates, collects static files, and
sends gunicorn a HUP so it reloads workers without downtime. Production reads
its variables from a `.env` file in that directory, the same way local does.

Gunicorn runs under systemd as `windwardapps.com.service`; nginx proxies to
it on port 9100 and serves `/static`, `/media`, `/iwredss` and `/.well-known`
from the app directory directly.
