# Delivery Management System - FastAPI

A complete RESTful API for a Delivery Management System built with FastAPI, following industry best practices and clean architecture principles.

## Features

- ✅ RESTful API endpoints
- ✅ Pydantic models for data validation
- ✅ FastAPI with SQL database (SQLite/PostgreSQL)
- ✅ OAuth2 with Password Flow authentication
- ✅ SQLModel relationships (One-to-Many, Many-to-Many)
- ✅ Alembic database migrations
- ✅ Email verification
- ✅ Password reset mechanisms
- ✅ Email notification system
- ✅ SMS notification system
- ✅ Celery workers for background tasks
- ✅ Docker containerization
- ✅ Docker Compose setup
- ✅ Production deployment ready

## Project Structure

```
.
├── app/
│   ├── api/              # API route handlers
│   │   ├── auth.py      # Authentication endpoints
│   │   ├── users.py     # User management endpoints
│   │   ├── deliveries.py # Delivery management endpoints
│   │   └── dependencies.py # Shared dependencies
│   ├── core/            # Core configuration
│   │   ├── config.py    # Application settings
│   │   ├── database.py  # Database connection
│   │   └── security.py  # Security utilities
│   ├── models/         # SQLAlchemy models
│   │   ├── user.py     # User model
│   │   └── delivery.py # Delivery model
│   ├── schemas/        # Pydantic schemas
│   │   ├── user.py     # User schemas
│   │   ├── delivery.py # Delivery schemas
│   │   └── auth.py     # Auth schemas
│   ├── services/       # Business logic services
│   │   ├── email_service.py # Email service
│   │   └── sms_service.py   # SMS service
│   ├── tasks/          # Celery tasks
│   │   ├── celery_app.py
│   │   ├── email_tasks.py
│   │   └── sms_tasks.py
│   └── main.py         # FastAPI application
├── alembic/            # Database migrations
├── nginx/              # Nginx configuration
├── scripts/            # Deployment scripts
├── docker-compose.yml  # Production Docker Compose
├── docker-compose.dev.yml # Development Docker Compose
├── docker-compose.prod.yml # Production Docker Compose
├── Dockerfile          # Docker image definition
└── requirements.txt   # Python dependencies
```

## Quick Start

### Local Development

1. **Install Dependencies**
```bash
pip install -r requirements.txt
```

2. **Configure Environment**
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. **Run Database Migrations**
```bash
alembic upgrade head
```

4. **Run the Application**
```bash
uvicorn app.main:app --reload
```

### Docker Development

```bash
docker-compose -f docker-compose.dev.yml up -d
```

### Docker Production

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed production deployment instructions.

```bash
cp .env.prod.example .env.prod
# Edit .env.prod with production values
./scripts/deploy.sh
```

## API Documentation

Once the application is running:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Authentication

The API uses OAuth2 with Password Flow. To authenticate:

1. Create a user via `POST /api/users/`
2. Login via `POST /api/auth/login` to get an access token
3. Use the token in the Authorization header: `Bearer <token>`

## Environment Variables

See `.env.example` for all available configuration options.

Key variables:
- `DATABASE_URL` - Database connection string
- `SECRET_KEY` - JWT secret key
- `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASSWORD` - Email configuration
- `SMS_PROVIDER`, `SMS_API_KEY`, `SMS_API_SECRET` - SMS configuration

## Database Migrations

```bash
# Create a new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

## Docker Commands

```bash
# Build images
docker-compose build

# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Remove volumes (CAUTION: deletes data)
docker-compose down -v
```

## Production Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for comprehensive production deployment guide.

---

## Detailed Technical Implementation

### 1. RESTful API with Clean Architecture

**1.1 Code Location and Explanation:**

- **`app/main.py`**: Main FastAPI application entry point. Creates the FastAPI instance, includes routers, sets up CORS middleware, and handles global exception handling. Uses dependency injection pattern throughout.

- **`app/api/`**: Contains all API route handlers organized by domain:
  - `auth.py`: Authentication endpoints (`/api/auth/login`, `/api/auth/me`, `/api/auth/verify-email`, `/api/auth/reset-password`)
  - `users.py`: User CRUD operations (`/api/users/`)
  - `deliveries.py`: Delivery management endpoints (`/api/deliveries/`)
  - `dependencies.py`: Shared dependencies like `get_current_user` for authentication

- **Clean Architecture Pattern**: 
  - **Models** (`app/models/`): Database layer (SQLAlchemy)
  - **Schemas** (`app/schemas/`): Data validation layer (Pydantic)
  - **API** (`app/api/`): Presentation layer (FastAPI routes)
  - **Services** (`app/services/`): Business logic layer
  - **Core** (`app/core/`): Configuration and utilities

This separation ensures each layer has a single responsibility, making the codebase maintainable, testable, and scalable.

---

### 2. Pydantic Models for Type Safety and Validation

**2.1 Code Location and Explanation:**

- **`app/schemas/user.py`**: Defines Pydantic models for User operations:
  - `UserBase`: Base fields (name, email)
  - `UserCreate`: Extends UserBase with password for registration
  - `UserUpdate`: Optional fields for partial updates
  - `User`: Response model with id
  - `ShowUser`: Detailed user response with deliveries list

- **`app/schemas/delivery.py`**: Defines Pydantic models for Delivery operations:
  - `DeliveryBase`: Core delivery fields
  - `DeliveryCreate`: For creating new deliveries
  - `DeliveryUpdate`: Optional fields for updates
  - `Delivery`: Response model with id and user_id
  - `ShowDelivery`: Complete delivery information

- **`app/schemas/auth.py`**: Authentication-related schemas:
  - `Login`: Login request model
  - `Token`: Token response model
  - `EmailVerificationRequest`: Email verification request
  - `PasswordResetRequest`: Password reset request

**How it works**: FastAPI automatically validates incoming requests against these Pydantic models. Invalid data returns 422 errors with detailed validation messages. Type hints ensure IDE autocomplete and catch errors at development time.

---

### 3. FastAPI with SQL Databases using Dependency Injection

**3.1 Code Location and Explanation:**

- **`app/core/database.py`**: 
  - Creates SQLAlchemy engine from `DATABASE_URL` (supports SQLite and PostgreSQL)
  - Defines `SessionLocal` for database sessions
  - Implements `get_db()` dependency function that yields a database session and automatically closes it after use

- **Usage in API endpoints**: Every endpoint that needs database access uses `db: Session = Depends(get_db)`. FastAPI's dependency injection system:
  1. Calls `get_db()` when the endpoint is hit
  2. Yields a database session
  3. Uses the session in the endpoint
  4. Automatically closes the session when done (via `finally` block)

- **Example from `app/api/users.py`**:
```python
def create_user(..., db: Session = Depends(get_db)):
    # db is automatically provided by FastAPI
    db_user = User(name=name, email=email, password=hashed_pw)
    db.add(db_user)
    db.commit()
```

**Benefits**: 
- Automatic resource management (sessions are always closed)
- Easy testing (can mock `get_db` dependency)
- Consistent database access pattern across all endpoints
- Supports both SQLite (development) and PostgreSQL (production) via `DATABASE_URL`

---

### 4. SQLModel Relationships (One-to-Many)

**4.1 Code Location and Explanation:**

- **`app/models/user.py`**: 
  - Defines `User` model with `deliveries` relationship: `deliveries = relationship("Delivery", back_populates="user", cascade="all, delete-orphan")`
  - This creates a one-to-many relationship where one User can have many Deliveries
  - `cascade="all, delete-orphan"` means if a user is deleted, all their deliveries are automatically deleted

- **`app/models/delivery.py`**: 
  - Defines `Delivery` model with foreign key: `user_id = Column(Integer, ForeignKey("users.id"))`
  - Defines reverse relationship: `user = relationship("User", back_populates="deliveries")`
  - The `ForeignKey` creates the database constraint linking deliveries to users

- **`app/schemas/user.py`**: 
  - `ShowUser` schema includes `deliveries: List[Delivery] = []` to return user with all their deliveries

**How it works**: 
- When you query a User, you can access `user.deliveries` to get all deliveries
- When you query a Delivery, you can access `delivery.user` to get the owner
- SQLAlchemy automatically handles the JOIN queries
- The relationship is bidirectional (back_populates) so changes are synchronized

**Example usage**:
```python
user = db.query(User).filter(User.id == 1).first()
# Access all deliveries: user.deliveries
# Each delivery can access its user: delivery.user
```

---

### 5. Alembic Database Migrations

**5.1 Code Location and Explanation:**

- **`alembic/`**: Directory containing migration files and configuration
  - `alembic.ini`: Alembic configuration file
  - `env.py`: Migration environment setup that imports models and database URL
  - `versions/`: Contains migration revision files (auto-generated)

- **`alembic/env.py`**: 
  - Imports `Base` metadata from `app.core.database`
  - Imports all models (`User`, `Delivery`) so Alembic can detect schema changes
  - Sets database URL from `settings.DATABASE_URL`
  - Configures online/offline migration modes

**How it works**:
1. **Create migration**: `alembic revision --autogenerate -m "description"`
   - Alembic compares current models with database schema
   - Generates migration file with SQL commands to update database

2. **Apply migration**: `alembic upgrade head`
   - Executes pending migrations in order
   - Updates database schema to match models

3. **Rollback**: `alembic downgrade -1`
   - Reverts last migration
   - Useful for fixing issues

**Benefits**:
- Version control for database schema
- Safe schema updates (can rollback)
- Team collaboration (everyone has same schema)
- Production-safe deployments (test migrations first)

---

### 6. OAuth2 with Password Flow Authentication

**6.1 Code Location and Explanation:**

- **`app/core/security.py`**: 
  - `hash_password()`: Hashes passwords using `pwdlib` (Argon2 algorithm)
  - `verify_password()`: Verifies plain password against hash
  - `create_access_token()`: Creates JWT token with user email and expiration
  - `decode_access_token()`: Decodes and validates JWT token

- **`app/api/dependencies.py`**: 
  - `oauth2_scheme`: OAuth2PasswordBearer instance that extracts token from Authorization header
  - `get_current_user()`: Dependency function that:
    1. Extracts token from request header
    2. Decodes token to get user email
    3. Queries database for user
    4. Returns user or raises 401 error

- **`app/api/auth.py`**: 
  - `POST /api/auth/login`: Accepts email/password, verifies credentials, returns JWT token
  - `GET /api/auth/me`: Protected endpoint using `Depends(get_current_user)` to return current user info

**How it works**:
1. User logs in with email/password → `/api/auth/login`
2. Server verifies password, creates JWT token with user email
3. Client stores token, sends in header: `Authorization: Bearer <token>`
4. Protected endpoints use `get_current_user` dependency to validate token and get user
5. Token expires after 30 minutes (configurable)

**Email Verification** (`app/api/auth.py`):
- `POST /api/auth/request-verification`: Generates verification token, stores in database, sends email
- `GET /api/auth/verify-email?token=...`: Validates token, marks user as verified

**Password Reset** (`app/api/auth.py`):
- `POST /api/auth/request-password-reset`: Generates reset token, sends email with link
- `POST /api/auth/reset-password`: Validates token, updates password

---

### 7. Email and SMS Notification Systems

**7.1 Code Location and Explanation:**

- **`app/services/email_service.py`**: 
  - `EmailService` class handles all email operations
  - `send_email()`: Generic email sender using SMTP
  - `send_verification_email()`: Sends email verification link
  - `send_password_reset_email()`: Sends password reset link
  - `send_delivery_notification()`: Sends delivery status updates
  - Uses SMTP settings from `app/core/config.py`

- **`app/services/sms_service.py`**: 
  - `SMSService` class handles SMS operations
  - Supports Twilio and AWS SNS providers
  - `send_sms()`: Generic SMS sender
  - `send_delivery_notification()`: Sends delivery updates via SMS
  - Uses SMS settings from `app/core/config.py`

- **Integration in `app/api/deliveries.py`**: 
  - When delivery is created/updated, automatically calls:
    - `email_service.send_delivery_notification()` to notify user via email
    - `sms_service.send_delivery_notification()` to notify user via SMS

**How it works**:
1. Delivery event occurs (create/update)
2. API endpoint calls notification services
3. Services use configured SMTP/SMS credentials
4. If not configured, services print to console (development mode)
5. Notifications sent asynchronously via Celery (or synchronously if Celery not running)

**Configuration**: Set `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASSWORD` in `.env` for email. Set `SMS_PROVIDER`, `SMS_API_KEY`, `SMS_API_SECRET` for SMS.

---

### 8. Celery Workers for Background Tasks

**8.1 Code Location and Explanation:**

- **`app/tasks/celery_app.py`**: 
  - Creates Celery application instance
  - Configures Redis as message broker and result backend
  - Sets up task serialization (JSON format)

- **`app/tasks/email_tasks.py`**: 
  - Defines Celery tasks for email operations:
    - `send_email_task`: Generic email task
    - `send_verification_email_task`: Email verification task
    - `send_password_reset_email_task`: Password reset email task
    - `send_delivery_notification_email_task`: Delivery notification task

- **`app/tasks/sms_tasks.py`**: 
  - Defines Celery tasks for SMS operations:
    - `send_sms_task`: Generic SMS task
    - `send_delivery_notification_sms_task`: Delivery SMS task

**How it works**:
1. API endpoint calls Celery task (e.g., `send_email_task.delay(...)`)
2. Task is queued in Redis
3. Celery worker picks up task from queue
4. Worker executes task (sends email/SMS)
5. Result stored in Redis backend

**Benefits**:
- Non-blocking: API responds immediately, email/SMS sent in background
- Scalable: Can run multiple workers to handle more tasks
- Reliable: Failed tasks can be retried
- Monitoring: Can track task status and results

**Running Celery**: `celery -A app.tasks.celery_app worker --loglevel=info`

---

### 9. Docker Containerization

**9.1 Code Location and Explanation:**

- **`Dockerfile`**: 
  - Multi-stage build: Uses `python:3.11-slim` as base
  - Stage 1 (builder): Installs dependencies
  - Stage 2 (runtime): Copies only necessary files, smaller final image
  - Exposes port 8000
  - Runs `uvicorn` command to start FastAPI app

- **`docker-compose.yml`**: Main compose file defining all services:
  - `db`: PostgreSQL database container
  - `redis`: Redis container for Celery
  - `web`: FastAPI application container
  - `celery`: Celery worker container
  - `celery-beat`: Celery scheduler container

- **`docker-compose.dev.yml`**: Development configuration with:
  - Volume mounts for hot reload
  - Exposed ports for local access
  - Simplified setup

- **`docker-compose.prod.yml`**: Production configuration with:
  - Nginx reverse proxy
  - SSL/HTTPS support
  - Password-protected Redis
  - Health checks
  - Restart policies

- **`.dockerignore`**: Excludes unnecessary files from Docker build (`.env`, `__pycache__`, etc.)

**How it works**:
1. `docker-compose build`: Builds Docker images from Dockerfile
2. `docker-compose up`: Starts all containers
3. Containers communicate via Docker network
4. Volumes persist database data
5. Nginx routes traffic to FastAPI app

**Benefits**:
- Consistent environment across dev/staging/production
- Easy deployment (one command)
- Isolated services (database, cache, app)
- Scalable (can run multiple app instances)

---

### 10. Production Deployment

**10.1 Code Location and Explanation:**

- **`nginx/nginx.conf`**: 
  - Reverse proxy configuration
  - Routes HTTP (port 80) and HTTPS (port 443) traffic to FastAPI app
  - Handles SSL/TLS termination
  - Load balancing support (can add multiple upstream servers)

- **`scripts/deploy.sh`**: 
  - Automated deployment script
  - Builds Docker images
  - Runs database migrations
  - Starts all services
  - Checks service health

- **`scripts/backup.sh`**: 
  - Creates PostgreSQL database backup
  - Saves to `backups/` directory with timestamp

- **`scripts/restore.sh`**: 
  - Restores database from backup file
  - Useful for disaster recovery

- **`.env.prod.example`**: 
  - Template for production environment variables
  - Includes all required settings (database, Redis, SMTP, SMS, secrets)

- **`docker-compose.prod.yml`**: 
  - Production-optimized configuration:
    - Multiple FastAPI workers (4 workers for concurrency)
    - Health checks for all services
    - Automatic restarts on failure
    - Password-protected Redis
    - Nginx for HTTPS and load balancing

**Deployment Process**:
1. Configure `.env.prod` with production values
2. Set up SSL certificates in `nginx/ssl/`
3. Run `./scripts/deploy.sh` or `docker-compose -f docker-compose.prod.yml up -d`
4. Run migrations: `docker-compose -f docker-compose.prod.yml run --rm web alembic upgrade head`
5. Verify services: `docker-compose -f docker-compose.prod.yml ps`

**Security Features**:
- Strong passwords for database and Redis
- SSL/HTTPS encryption
- Secret key management via environment variables
- Firewall-ready (only expose ports 80, 443)
- Regular backups via cron jobs

**Scalability**:
- Horizontal scaling: `docker-compose up -d --scale web=3` (3 app instances)
- Vertical scaling: Adjust worker count in docker-compose
- Load balancing: Nginx distributes traffic across instances

---

## License

MIT
