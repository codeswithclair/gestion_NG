# Noreste Grill

Flask application for restaurant staff workflows, including login, reservations, waitlist, tables, promotions, users, and dashboards.

## Local setup

Create and activate a virtual environment, then install dependencies:

```powershell
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

Set the database environment variables before running the app:

```powershell
$env:DB_HOST="localhost"
$env:DB_USER="root"
$env:DB_PASSWORD="your_mysql_password"
$env:DB_NAME="noreste_grill"
```

Run the app:

```powershell
python -m backend.test_app
```

The app starts at `http://127.0.0.1:5000`.

## Versions

See [VERSIONES.md](VERSIONES.md) for the tools, versions, installation steps, and the reason those versions were used.
