# AutoSOC

**AutoSOC** is an Automated Security Operations Center (SOC) middleware built with Clean Architecture principles in Python.

## Architecture Overview

```
src/
├── domain/           # Entities, value objects, repository interfaces
├── application/      # Use cases, DTOs, application services
├── infrastructure/   # DB repositories, external connectors, AI engine
└── presentation/     # FastAPI routers, schemas, dependencies
```

### Layers

- **Domain**: Pure Python dataclasses for `Case`, `ClientTenant`, `SystemConnector`, `CommunicationChannel` plus enums and abstract repository interfaces.
- **Application**: Use cases orchestrate domain logic. Services for AI analysis (`IAIEngineService`), notifications (`NotificationService`), and external sync (`SyncService`).
- **Infrastructure**: SQLAlchemy async repositories, Ollama LLM adapter, ServiceNow/Jira connectors, Email/Slack channels.
- **Presentation**: FastAPI app with versioned REST API (`/api/v1/`).

## Setup

### Requirements

- Python 3.11+
- (Optional) Docker & Docker Compose for PostgreSQL + Ollama

### Local Development (SQLite)

```bash
pip install -e ".[dev]"
uvicorn src.presentation.api.main:app --reload
```

### Docker Compose

```bash
docker compose up
```

API available at `http://localhost:8000`. Docs at `http://localhost:8000/docs`.

## Running Tests

```bash
pytest tests/ -v
```

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check |
| POST | `/api/v1/cases/` | Create case |
| GET | `/api/v1/cases/` | List cases (by tenant) |
| GET | `/api/v1/cases/{id}` | Get case |
| PATCH | `/api/v1/cases/{id}` | Update case |
| POST | `/api/v1/cases/{id}/close` | Close case |
| POST | `/api/v1/cases/{id}/reopen` | Reopen case |
| POST | `/api/v1/cases/{id}/assign` | Assign case |
| POST | `/api/v1/tenants/` | Create tenant |
| GET | `/api/v1/tenants/` | List tenants |
| GET | `/api/v1/tenants/{id}` | Get tenant |
| PATCH | `/api/v1/tenants/{id}` | Update tenant |
| POST | `/api/v1/connectors/` | Register system connector |
| POST | `/api/v1/channels/` | Register communication channel |
| POST | `/api/v1/webhooks/{connector_id}` | Inbound webhook |
