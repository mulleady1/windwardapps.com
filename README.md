# windwardapps.com

Django 6.1 site for Windward Apps. One Django app (`app`), one settings module,
SQLite, htmx 4 for the forms, hCaptcha, and a Mailgun-style HTTP API for email.

Django 6.1 is a regular release; move to 6.2 LTS when it ships (April 2027).

## Layout

```
manage.py            Django entry point (defaults to project.settings)
project/             settings.py, urls.py, wsgi.py
app/                 the whole site: models, views, forms, templates, static
  templates/app/     page templates; news/ for the blog, email/ for emails
  static/app/        site.css, images, vendored htmx.min.js, forms.js (captcha mounting)
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

## Forms

The contact and newsletter forms post with htmx. Each form is a template
partial (`{% partialdef %}`); the view answers with the re-rendered form on
a 422, or the success partial on a 200, and htmx swaps the form in place.

Every public submission passes three checks in `GuardedFormView`: a honeypot
field (bots that fill it get a fake success), a rate limit of 5 per IP and 30
site-wide per hour per form (backed by a file cache in `.cache/`), and
hCaptcha when `CAPTCHA_ENFORCE` is on. Newsletter signups never send email.

## Configuration

| Variable | Purpose |
| --- | --- |
| `DEBUG` | `1` for local development. Off by default. |
| `SECRET_KEY` | Required when `DEBUG` is off. |
| `ALLOWED_HOSTS` | Comma separated. Defaults to `windwardapps.com,www.windwardapps.com`. |
| `STATIC_ROOT` | Where `collectstatic` writes. Defaults to `./static`. |
| `CONTACT_EMAIL` | Recipient of contact-form messages. |
| `EMAIL_API_URL`, `EMAIL_API_KEY` | Email API endpoint and key. |
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
from the app directory directly. Application logs go to stderr, so read them
with `journalctl -u windwardapps.com`.
