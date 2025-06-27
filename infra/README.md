# ProPulse Infrastructure

Infrastructure and deployment configurations for the ProPulse system.

## 📁 Directory Structure

```
infra/
├── gcp/                    # Google Cloud Platform configs
│   ├── backend/           # Backend service
│   │   ├── Dockerfile    # Container config
│   │   └── deploy.sh     # Deployment script
│   │
│   └── frontend/         # Frontend service
│       ├── Dockerfile    # Container config
│       └── deploy.sh     # Deployment script
│
├── terraform/            # Infrastructure as Code
│   ├── main.tf          # Main configuration
│   ├── variables.tf     # Variable definitions
│   └── outputs.tf       # Output definitions
│
└── scripts/             # Utility scripts
    ├── setup.sh         # Environment setup
    └── cleanup.sh       # Resource cleanup
```

## 🚀 Deployment

### Prerequisites
- Google Cloud SDK
- Terraform >= 1.0
- Docker

### Environment Setup

1. Initialize GCP project:
   ```bash
   ./scripts/setup.sh init
   ```

2. Configure environment:
   ```bash
   ./scripts/setup.sh configure
   ```

### Backend Deployment

1. Build container:
   ```bash
   cd gcp/backend
   docker build -t gcr.io/[PROJECT_ID]/propulse-backend .
   ```

2. Deploy to Cloud Run:
   ```bash
   ./deploy.sh
   ```

### Frontend Deployment

1. Build container:
   ```bash
   cd gcp/frontend
   docker build -t gcr.io/[PROJECT_ID]/propulse-frontend .
   ```

2. Deploy to Cloud Run:
   ```bash
   ./deploy.sh
   ```

## 🏗️ Infrastructure

### Cloud Resources
- Cloud Run services
- Cloud Storage buckets
- Cloud Logging
- Cloud Monitoring

### Security
- IAM roles and permissions
- VPC configuration
- Secret management
- SSL certificates

### Monitoring
- Custom dashboards
- Alert policies
- Log-based metrics
- Uptime checks

## 📊 Scaling

### Horizontal Scaling
- Auto-scaling policies
- Load balancing
- Instance groups

### Resource Management
- CPU allocation
- Memory limits
- Concurrency settings

## 🔒 Security

### Access Control
- Service accounts
- API keys
- OAuth 2.0 config

### Network Security
- Firewall rules
- VPC peering
- Cloud Armor

## 📝 Logging

### Log Types
- Application logs
- Access logs
- Error logs
- Audit logs

### Log Management
- Log retention
- Log exports
- Log-based metrics

## 🔄 Continuous Deployment

### GitHub Actions
- Build pipeline
- Test automation
- Deployment workflow

### Monitoring
- Deployment health
- Rollback procedures
- Version tracking

## 🧪 Testing

### Infrastructure Tests
```bash
cd terraform
terraform plan -var-file=test.tfvars
```

### Load Testing
```bash
./scripts/loadtest.sh
```

## 📚 Documentation

- Keep deployment docs updated
- Document infrastructure changes
- Maintain runbooks
- Track configuration updates 