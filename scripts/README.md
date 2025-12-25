# Deployment Scripts

## Available Scripts

### deploy.sh
Deploys the application to production.
```bash
./scripts/deploy.sh
```

### backup.sh
Creates a database backup.
```bash
./scripts/backup.sh
```

### restore.sh
Restores a database from backup.
```bash
./scripts/restore.sh backups/db_backup_YYYYMMDD_HHMMSS.sql
```

### init-db.sh
Initializes the database with migrations.
```bash
./scripts/init-db.sh
```

## Making Scripts Executable

On Linux/Mac:
```bash
chmod +x scripts/*.sh
```

On Windows (PowerShell):
```powershell
# Scripts can be run directly with bash if Git Bash or WSL is installed
bash scripts/deploy.sh
```

