import os

folders = [
    "app",
    "app/core",
    "app/db",
    "app/db/migrations",
    "app/models",
    "app/schemas",
    "app/crud",
    "app/api",
    "app/api/v1",
    "app/services",
    "app/tests"
]

files = [
    "app/__init__.py",
    "app/main.py",
    "app/core/__init__.py",
    "app/core/config.py",
    "app/core/security.py",
    "app/core/celery_utils.py",
    "app/db/__init__.py",
    "app/db/base.py",
    "app/db/session.py",
    "app/models/__init__.py",
    "app/models/user.py",
    "app/models/delivery.py",
    "app/schemas/__init__.py",
    "app/schemas/user.py",
    "app/schemas/delivery.py",
    "app/crud/__init__.py",
    "app/crud/user.py",
    "app/crud/delivery.py",
    "app/api/__init__.py",
    "app/api/deps.py",
    "app/api/v1/__init__.py",
    "app/api/v1/user.py",
    "app/api/v1/delivery.py",
    "app/services/__init__.py",
    "app/services/email.py",
    "app/services/sms.py",
    "app/services/celery_tasks.py",
    "app/tests/__init__.py"
]

for folder in folders:
    os.makedirs(folder, exist_ok=True)

for file in files:
    with open(file, "w", encoding="utf-8") as f:
        pass  # create empty file

print("Project structure created successfully.")