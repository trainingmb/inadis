# Migrations

This repo uses Flask-Migrate / Alembic for database migrations.

To generate and apply migrations locally:

1. Activate your virtualenv and install requirements:

```powershell
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Set the Flask app and database URL (example sqlite):

```powershell
$env:FLASK_APP = "migrate_app.py"
$env:DATABASE_URL = "sqlite:///instance/file.db"
```

3. If you haven't initialized migrations yet, run:

```powershell
flask db init
```

4. Create a migration (autogenerate):

```powershell
flask db migrate -m "Add user_creation_progress"
```

5. Apply the migration:

```powershell
flask db upgrade
```

If you prefer to use the included manual migration file, you can skip step 4 and run `flask db upgrade` to apply the existing revision (ensure `migrations/` exists and `env.py` is present).

On PythonAnywhere:

- Set your `DATABASE_URL` env var to the MySQL connection string.
- Install requirements into the webapp virtualenv.
- Run the same `flask db upgrade` command in a bash console on PythonAnywhere (backup DB before running migrations).
