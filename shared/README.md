# ProPulse Shared Resources

Common assets and configurations shared between frontend and backend services.

## 📁 Directory Structure

```
shared/
├── sample_rfps/           # Example RFP documents
│   ├── tech/             # Technology sector
│   ├── healthcare/       # Healthcare sector
│   └── finance/         # Financial sector
│
├── personas.json         # Writing style definitions
├── mcp_schemas/         # Model Context Protocol schemas
│   ├── proposal.json    # Proposal structure
│   ├── agent.json      # Agent communication
│   └── validation.json # Validation rules
│
└── templates/          # Document templates
    ├── base/          # Base templates
    └── custom/        # Client-specific templates
```

## 📝 Personas

The `personas.json` file defines different writing styles:

```json
{
  "technical": {
    "tone": "professional",
    "complexity": "high",
    "formality": "formal"
  },
  "business": {
    "tone": "persuasive",
    "complexity": "medium",
    "formality": "semi-formal"
  },
  "executive": {
    "tone": "confident",
    "complexity": "low",
    "formality": "formal"
  }
}
```

## 📋 MCP Schemas

### Proposal Schema
- Document structure
- Section requirements
- Content validation rules

### Agent Schema
- Inter-agent communication
- Message formats
- State management

### Validation Schema
- Content requirements
- Compliance rules
- Quality metrics

## 📄 Templates

### Base Templates
- Standard proposal structure
- Common sections
- Default formatting

### Custom Templates
- Client-specific layouts
- Industry-specific content
- Brand guidelines

## 🔄 Usage

1. Import shared resources:
   ```python
   from shared.mcp_schemas import ProposalSchema
   from shared.personas import get_persona
   ```

2. Load templates:
   ```python
   from shared.templates import load_template
   template = load_template("base/standard.docx")
   ```

3. Access sample RFPs:
   ```python
   from shared.sample_rfps import get_sample
   rfp = get_sample("tech/software.pdf")
   ```

## 🔒 Security

- All sensitive data must be encrypted
- Templates should be version controlled
- Access logs are maintained
- Regular security audits

## 📚 Documentation

- Keep schemas up to date
- Document template changes
- Track persona modifications
- Maintain changelog 