# ProPulse: Enterprise Proposal Assistant

ProPulse is a multi-agent system that automates enterprise proposal generation using Google's Gemini 2.5 and ADK. The system leverages specialized AI agents to retrieve relevant past work, generate custom proposals, and validate content accuracy.

## 🏗️ Architecture

```mermaid
graph TD
    A[Client Browser] -->|Access| B[Streamlit Frontend]
    B -->|API Requests| C[FastAPI Backend]
    C -->|Orchestrates| D[Agent System]
    
    subgraph "Agent System"
        D -->|1. Find Similar| E[Retriever Agent]
        D -->|2. Generate| F[Writer Agent]
        D -->|3. Validate| G[Verifier Agent]
        E -->|Past Content| F
        F -->|Draft| G
        G -->|Validated| D
        
        E -->|Query| DB[(Proposals DB)]
        DB -->|Results| E
        
        API[Gemini 2.5] -->|LLM API| D
        API -->|Generation| F
        API -->|Validation| G
    end
```

## 🤖 Agent Collaboration

1. **Retriever Agent**
   - Analyzes incoming RFP requirements
   - Searches historical proposals
   - Extracts relevant sections and insights

2. **Writer Agent**
   - Uses retrieved content as context
   - Generates new proposal sections
   - Adapts tone using defined personas

3. **Verifier Agent**
   - Validates technical accuracy
   - Ensures compliance with RFP
   - Checks for consistency

## 🚀 Setup Instructions

### Prerequisites
- Conda or Miniconda
- Git Bash (for Windows)
- Google Cloud account
- Gemini API access

### Environment Setup

#### Using Conda (Recommended)
1. Create conda environment:
   ```bash
   # In Git Bash
   conda env create -f environment.yml
   ```

2. Activate environment:
   ```bash
   # In Git Bash
   conda activate propulse
   ```

#### Using Python venv (Alternative)
1. Create and activate virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # or
   . venv/Scripts/activate   # Git Bash on Windows
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Environment Variables Setup

Create a `.env` file in the project root with the following variables:

```bash
# API Keys
GEMINI_API_KEY=your-gemini-api-key

# Service URLs
BACKEND_URL=http://localhost:8000
FRONTEND_URL=http://localhost:8501

# Google Cloud Configuration
GCP_PROJECT_ID=your-project-id
STORAGE_BUCKET=your-proposals-bucket

# Logging Configuration
LOG_LEVEL=INFO
ENABLE_AGENT_LOGGING=true

# Agent Configuration
MAX_TOKENS_PER_REQUEST=8192
TEMPERATURE=0.7
TOP_P=0.95

# Security
ENABLE_AUTH=false
ALLOWED_ORIGINS=http://localhost:8501,https://your-domain.com
```

### Local Development
1. Clone the repository:
   ```bash
   git clone https://github.com/nerdy1texan/Propulse.git
   cd enterprise-proposal-assistant
   ```

2. Set up environment variables:
   ```bash
   # Copy the environment variables above into .env file
   ```

3. Start services:
   ```bash
   # Terminal 1: Backend
   cd backend
   uvicorn main:app --reload --port 8000

   # Terminal 2: Frontend
   cd frontend
   streamlit run main.py
   ```

### Cloud Deployment
1. Set up Google Cloud project
2. Configure Cloud Run
3. Deploy using provided scripts in `infra/gcp/`

## 📁 Project Structure

```
enterprise-proposal-assistant/
├── backend/         # FastAPI + Google ADK agents
├── frontend/        # Streamlit UI
├── shared/          # Common assets and schemas
├── infra/          # Deployment configurations
└── .github/        # CI/CD workflows
```

## 🔑 Environment Variables

Required environment variables:
- `GEMINI_API_KEY`: Google Gemini API key
- `BACKEND_URL`: FastAPI backend URL
- `GCP_PROJECT_ID`: Google Cloud project ID
- `STORAGE_BUCKET`: GCS bucket for proposals

## 📚 Documentation

- [Backend Documentation](./backend/README.md)
- [Frontend Documentation](./frontend/README.md)
- [Infrastructure Guide](./infra/README.md)

## 📝 License

MIT License - see LICENSE file for details
