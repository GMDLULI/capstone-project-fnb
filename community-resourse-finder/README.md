# CommunityResourseFinder app

## Run the app

### uv

Run as a desktop app:

```bash
uv run flet run
```
# Community Resource Finder

A desktop app that helps people find local community resources such as clinics, free courses and job boards. Users create an account, log in, and browse a searchable list of resources. Clicking a resource opens its website, or a details page if it has no website.

The project has two parts that talk to each other over HTTP:

- **Backend:** a FastAPI REST API that serves resources from a JSON file and handles accounts.
- **Frontend:** a Flet (Python) app with login, sign-up, forgot-password, home and details screens.

```
resource.json  ->  FastAPI backend (REST API)  ->  Flet app (UI)
users.json     ->  /auth/* and /resources       ->  login, home, details
```

## Features

- Sign up, log in and reset a password
- Passwords are stored as salted PBKDF2 hashes, never in plain text
- Accounts are saved to `users.json`, so they survive restarts
- Browse resources as cards and search by name, area or description
- Click a card to visit the resource's website, or view a details page when there is no website
- Friendly error messages when the server is unreachable or input is invalid

## Tech stack

- Python 3.10 or newer
- [Flet](https://flet.dev) 1.0 for the UI
- [FastAPI](https://fastapi.tiangolo.com) and Uvicorn for the API
- [httpx](https://www.python-httpx.org) for the UI-to-API calls
- JSON files for storage

## Project structure

Adjust the folder names to match your project.

```
community-resource-finder/
├── backend/
│   ├── main.py              # FastAPI app (resources + auth endpoints)
│   └── data/
│       ├── resource.json    # the resources you curate
│       └── users.json       # registered users (created and updated by the API)
└── src/
    ├── main.py              # starts the Flet app and handles routing
    ├── api.py               # all HTTP calls to the backend
    └── pages/
        ├── login.py
        ├── signin.py        # sign-up screen
        ├── home.py          # searchable list of resource cards
        ├── resource_detail.py
        ├── reset_password.py  # forgot-password dialog
        └── components.py    # shared colours and the resource card
```

## Getting started

### 1. Prerequisites

- Python 3.10+
- Git (optional)

### 2. Create a virtual environment and install dependencies

From the project root:

```bash
python -m venv .venv
```

Activate it:

```bash
# Windows (PowerShell)
.venv\Scripts\Activate.ps1

# Windows (cmd)
.venv\Scripts\activate.bat

# macOS / Linux
source .venv/bin/activate
```

Install the packages:

```bash
pip install flet fastapi "uvicorn[standard]" httpx
```

### 3. Prepare the data files

`backend/data/resource.json` holds your resources. Every entry needs a unique integer `id`:

```json
[
  {
    "id": 1,
    "name": "Brakpan Jobs",
    "category": "job",
    "area": "Brakpan",
    "description": "Local job listings for the Brakpan area.",
    "phone": "",
    "website": "https://brakpanjobs.org"
  }
]
```

- `category` is one of your own labels, for example `clinic`, `course` or `job`.
- `phone` and `website` are optional. Leave them as `""` if you don't have one.
- A resource **with** a `website` opens that link when clicked. A resource **without** one opens the details page.

`backend/data/users.json` should start as an empty object:

```json
{}
```

### 4. Run the backend

Open a terminal, activate the virtual environment, and run:

```bash
cd backend
uvicorn main:app --reload
```

The API is now at `http://127.0.0.1:8000`. Open `http://127.0.0.1:8000/docs` for interactive API documentation where you can try every endpoint.

### 5. Run the app

Open a **second** terminal, activate the virtual environment, and run:

```bash
cd src
python main.py
```

Keep both terminals open. The app needs the backend running to log in or load resources.

### 6. Use it

1. Click **Create an account**, enter an email and a password (at least 6 characters), and sign up.
2. You are taken to the home screen. Search by typing and pressing Enter or clicking **Search**.
3. Click a card to open the website or the details page.
4. Use **Log out** to return to the login screen.

## API reference

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | API status and a list of endpoints |
| GET | `/resources?q=&category=` | List resources, optionally filtered by search text or category |
| GET | `/resources/{id}` | Get one resource (404 if it doesn't exist) |
| POST | `/auth/register` | Create an account (409 if the email already exists) |
| POST | `/auth/login` | Log in with email and password (401 if invalid) |
| POST | `/auth/reset-password` | Set a new password for an email (404 if not found) |

Register, login and reset take a JSON body: `{"email": "you@example.com", "password": "secret123"}`.

## Troubleshooting

| Problem | Likely cause and fix |
|---|---|
| "Could not reach the server" in the app | The backend isn't running. Start it with `uvicorn main:app --reload` from the `backend` folder. |
| `409 Conflict` on `/auth/register` | That email is already registered. Log in instead. |
| `Internal Server Error` from the API | Check the uvicorn terminal for the traceback. The usual causes are invalid JSON in `resource.json` or `users.json`, or a missing field in a resource. Check a file with `python -m json.tool resource.json`. |
| Server won't start with a `users.json` error | `users.json` is corrupt or in the wrong format. Replace its contents with `{}`. |
| `ModuleNotFoundError: No module named 'pages'` | Run `python main.py` from inside the `src` folder, not from the project root. |
| Details page crashes with a list error | `api.get_resource` must call `/resources/{id}` and return one dictionary, not the full list from `get_resources`. |
| Opening a website does nothing | Check your Flet version with `pip show flet`. The code uses the Flet 1.0 `UrlLauncher`. |

## Known limitations

This is a learning project and is **not production-ready**:

- **Login has no tokens.** The server doesn't issue a session or JWT, so the home page is only protected in the UI, and `/resources` is public.
- **Password reset isn't verified.** Anyone who knows an email can set that account's password. A real version would email a one-time, expiring token.
- **Users are stored in a JSON file.** That is fine for a single local server but not for many users.
- **Don't commit `users.json`.** It contains emails and password hashes, so add `backend/data/users.json` to `.gitignore`.

## Roadmap

- Category filter buttons (Clinics, Courses, Jobs)
- JWT authentication and protected endpoints
- Email-based password reset with expiring tokens
- Move users and resources to SQLite
- Add and edit resources from inside the app
- A shared `theme.py` for colours across all screens
Run as a web app:

```bash
uv run flet run --web
```

For more details on running the app, refer to the [Getting Started Guide](https://flet.dev/docs/).

## Build the app

### Android

```bash
flet build apk -v
```

For more details on building and signing `.apk` or `.aab`, refer to the [Android Packaging Guide](https://flet.dev/docs/publish/android/).

### iOS

```bash
flet build ipa -v
```

For more details on building and signing `.ipa`, refer to the [iOS Packaging Guide](https://flet.dev/docs/publish/ios/).

### macOS

```bash
flet build macos -v
```

For more details on building macOS package, refer to the [macOS Packaging Guide](https://flet.dev/docs/publish/macos/).

### Linux

```bash
flet build linux -v
```

For more details on building Linux package, refer to the [Linux Packaging Guide](https://flet.dev/docs/publish/linux/).

### Windows

```bash
flet build windows -v
```

For more details on building Windows package, refer to the [Windows Packaging Guide](https://flet.dev/docs/publish/windows/).

### Web

```bash
flet build web -v
```

For more details on building Web app, refer to the [Web Packaging Guide](https://flet.dev/docs/publish/web/).
