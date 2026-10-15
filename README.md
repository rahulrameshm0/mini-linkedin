# Mini LinkedIn

A professional networking web application built with Django. Members can share updates, discover people, follow other members, and interact through likes and comments.

## Features

- Sign up, sign in, and sign out using Django authentication.
- Edit your profile headline, location, and biography.
- Delete your account from your own profile after entering your current password and confirming the permanent deletion.
- Browse and search members by username; follow or unfollow other members.
- Publish text posts with optional images; edit and delete your own posts.
- Browse a newest-first feed with 10 posts per page.
- Search posts by content or author username, and filter the feed to your own posts and people you follow.
- Like or unlike posts and add comments.
- Responsive community dashboard, post composer, profile pages, member directory, and authentication screens.
- Light and dark themes with a header toggle; the initial theme follows your system preference and your choice is saved in the browser.
- Manage records through Django's admin interface.

Post text supports up to 5,000 characters, comments up to 1,000 characters, and uploaded images up to 5 MiB. Forms use CSRF protection, and post edits and deletions are restricted to the author.

## Technology

- **Backend:** Python and Django 5.2
- **Database:** SQLite
- **Frontend:** Django templates, HTML, CSS, and JavaScript
- **Image handling:** Pillow
- **Deployment tools:** Gunicorn and Docker

Dependency version ranges are defined in `requirements.txt`. The Docker image uses Python 3.13.

## Local setup

Run these commands from the directory containing `manage.py`. Use Python 3.13 to match the Docker environment.

### 1. Create and activate a virtual environment

```sh
python3 -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell, activate it with:

```powershell
.venv\Scripts\Activate.ps1
```

### 2. Install dependencies and apply migrations

```sh
python -m pip install -r requirements.txt
python manage.py migrate
```

### 3. Start the development server

```sh
python manage.py runserver
```

Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/). You will be redirected to sign in; select **Join now** to create an account. The local database has been cleared for a fresh start; no demo users or default login credentials are provided.

To access the admin interface, create a superuser:

```sh
python manage.py createsuperuser
```

Then visit [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/).

## Using the application

1. Create an account and update your profile.
2. Publish a post, optionally attaching an image.
3. Create a second account to try following, likes, and comments between members.
4. Use the network page to find members and visit their profiles.
5. Switch to the following feed to see your posts and updates from members you follow.
6. Use **Dark mode** or **Light mode** in the header to change the theme.
7. To permanently remove your account, open **My profile → Delete account**, enter your current password, and check the confirmation box. This removes your profile, posts, comments, likes, and follow connections, then signs you out.

Account deletion removes database records. Uploaded image files are not automatically removed from storage when an account or post is deleted.

## Configuration

The application reads these environment variables directly; it does not automatically load a `.env` file.

| Variable | Default | Purpose |
| --- | --- | --- |
| `DJANGO_SECRET_KEY` | Development key in settings | Secret key; set a private, unique value in production. |
| `DJANGO_DEBUG` | `true` | Debug mode; set to `false` in production. |
| `DJANGO_ALLOWED_HOSTS` | `localhost,127.0.0.1,testserver` | Comma-separated hostnames, without spaces. |

SQLite data is stored in `db.sqlite3`. Uploaded images are stored in `media/posts/`. Source static assets live in `templates/static/`; `collectstatic` copies them into `staticfiles/` for deployment.

## Run with Docker

The included Dockerfile starts Django's development server on port 8000. Run migrations before starting the application. The volume below preserves the database and uploaded files between container runs; it also mounts the project source into the container.

```sh
docker build -t mini-linkedin .
docker run --rm -v "${PWD}:/app" mini-linkedin python manage.py migrate
docker run --rm -p 8000:8000 -v "${PWD}:/app" mini-linkedin
```

Open [http://localhost:8000/](http://localhost:8000/).

## Project structure

```text
mini_linkedin/
├── account/           # Authentication, profiles, and following
├── posts/             # Posts, feed, likes, and comments
├── mini_linkedin/     # Django settings and root URL configuration
├── templates/        # HTML templates
│   └── static/       # CSS, JavaScript, and bundled images
├── .agents/skills/   # Project-local frontend-design skill and license
├── media/            # User uploads (created as needed)
├── manage.py         # Django management commands
├── requirements.txt  # Python dependencies
├── Dockerfile        # Development container
└── README.md
```

## Checks and tests

```sh
python manage.py check
python manage.py test
```

## Production deployment

1. Set `DJANGO_SECRET_KEY`, `DJANGO_DEBUG=false`, and `DJANGO_ALLOWED_HOSTS` for your domain.
2. Apply migrations and collect static files:

   ```sh
   python manage.py migrate
   python manage.py collectstatic --noinput
   ```

3. Start the WSGI application with Gunicorn:

   ```sh
   gunicorn mini_linkedin.wsgi:application --bind 0.0.0.0:8000
   ```

4. Configure your web server to serve `/static/` from `staticfiles/` and `/media/` from `media/`. Django's development media serving is disabled when debug mode is off.
5. Configure HTTPS, secure session and CSRF cookies, and backups for the database and uploaded files.

The included Docker command uses the development server. Use a production server such as Gunicorn for deployment.

## Frontend design skill

The Anthropic `frontend-design` skill is included in [`.agents/skills/frontend-design/SKILL.md`](.agents/skills/frontend-design/SKILL.md), with its license alongside it. It provides design guidance for future frontend changes and is not a runtime dependency.

## Scope and implementation notes

Authentication uses Django's built-in `User` model and hashed passwords. The legacy `Accounts` model remains for migration compatibility. Job listings and private messaging are outside the current project's scope.
