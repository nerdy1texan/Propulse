# ProPulse Backend Service

The backend service handles all agent orchestration, API endpoints, and business logic for the ProPulse system.

## 📁 Directory Structure

```
backend/
├── agents/                 # AI Agent implementations
│   ├── retriever.py       # Finds relevant past proposals
│   ├── writer.py          # Generates proposal content
│   ├── verifier.py        # Validates proposal accuracy
│   └── base.py            # Common agent functionality
│
├── api/                   # FastAPI routes and endpoints
│   ├── proposals/         # Proposal-related endpoints
│   ├── auth/             # Authentication endpoints
│   └── health/           # Health check endpoints
│
├── core/                 # Core functionality
│   ├── config.py        # Configuration management
│   ├── logging.py       # Logging setup
│   └── utils.py         # Shared utilities
│
├── logs/                # Log files directory
│   ├── agent_logs/     # Agent-specific logs
│   └── api_logs/       # API request logs
│
└── main.py             # FastAPI application entry point
```

## 🚀 Getting Started

1. Install dependencies:
   ```bash
   pip install -r ../requirements.txt
   ```

2. Set up environment variables:
   ```bash
   cp ../.env.sample ../.env
   # Edit .env with your credentials
   ```

3. Start the server:
   ```bash
   uvicorn main:app --reload --port 8000
   ```

## 🤖 Agent System

### Retriever Agent
- Searches historical proposals
- Uses semantic similarity
- Extracts relevant sections

### Writer Agent
- Generates new content
- Adapts writing style
- Maintains consistency

### Verifier Agent
- Technical validation
- Compliance checking
- Quality assurance

## 🔌 API Endpoints

### Proposals
- `POST /api/v1/proposals/` - Create new proposal
- `GET /api/v1/proposals/{id}` - Get proposal details
- `PUT /api/v1/proposals/{id}` - Update proposal
- `DELETE /api/v1/proposals/{id}` - Delete proposal

### Authentication
- `POST /api/v1/auth/token` - Get access token
- `POST /api/v1/auth/refresh` - Refresh token

### Health
- `GET /health` - Service health check
- `GET /health/agents` - Agent system status

## 📊 Monitoring

- Agent performance metrics
- Token usage tracking
- Error rate monitoring
- Request latency stats

## 🔒 Security

- JWT authentication
- Role-based access control
- Rate limiting
- Input validation

## 🧪 Testing

Run tests:
```bash
pytest
```

Generate coverage report:
```bash
pytest --cov=app --cov-report=html
``` 