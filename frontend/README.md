# ProPulse Frontend

Streamlit-based frontend for the ProPulse enterprise proposal assistant.

## 📁 Directory Structure

```
frontend/
├── pages/                # Multi-page app components
│   ├── 01_dashboard.py  # Main dashboard
│   ├── 02_proposals.py  # Proposal management
│   └── 03_settings.py   # System settings
│
├── components/          # Reusable UI components
│   ├── proposal_form/  # Proposal creation form
│   ├── preview/        # Document preview
│   └── status/         # Status indicators
│
├── assets/             # Static assets
│   ├── css/           # Custom styles
│   └── img/           # Images and icons
│
└── main.py            # Streamlit entry point
```

## 🎨 Features

- Intuitive proposal creation interface
- Real-time preview of generated content
- Progress tracking and status updates
- Document template management
- User settings and preferences
- Dark/light theme support

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

3. Start the application:
   ```bash
   streamlit run main.py
   ```

## 🔧 Configuration

### Streamlit Config
Create `.streamlit/config.toml`:
```toml
[theme]
primaryColor = "#FF4B4B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"

[server]
port = 8501
```

## 📱 Responsive Design

- Desktop-first approach
- Mobile-friendly layouts
- Adaptive components
- Touch-friendly controls

## 🔒 Security Features

- Session management
- Input sanitization
- CSRF protection
- Secure cookie handling

## 🧪 Testing

Run tests:
```bash
pytest
```

## 📚 Component Library

### ProposalForm
```python
st.proposal_form(
    template_id: str,
    on_submit: Callable
)
```

### DocumentPreview
```python
st.document_preview(
    content: str,
    format: str = "docx"
)
```

### StatusIndicator
```python
st.status_indicator(
    status: str,
    message: str
)
```

## 🎨 Style Guide

- Use Streamlit native components when possible
- Follow Material Design principles
- Maintain consistent spacing
- Use approved color palette
- Keep UI elements minimal 