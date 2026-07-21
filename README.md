# 🛡️ Enterprise LLM & GenAI Security Gateway

> A FastAPI-based security gateway that protects Large Language Model (LLM) and Generative AI applications from common security threats such as prompt injection, API abuse, sensitive data exposure, and PII leakage.

---

## 📌 Overview

Enterprise AI applications require strong security controls before user requests reach an LLM and before AI-generated responses are returned to users.

This project implements a security gateway that sits between the client and the AI model to inspect requests, detect malicious content, validate API access, protect sensitive information, and provide a centralized security monitoring dashboard.

---

## ✨ Features

### 🔐 Authentication & Authorization
- JWT Authentication
- Role-Based Access Control (RBAC)
- Authorization Middleware

### 🔑 API Key Validation
- Validates incoming API keys
- Blocks unauthorized requests
- Logs API key violations

### 🛡️ Prompt Injection Detection
- Detects malicious prompt injection attempts
- Blocks suspicious prompts
- Logs detected attacks

### 👤 PII Detection
- Detects Personally Identifiable Information (PII)
- Prevents accidental exposure of sensitive user data
- Records security events

### 🚫 Sensitive Response Filtering
- Prevents confidential information leakage
- Blocks restricted AI responses
- Logs blocked responses

### 📊 Security Dashboard
- Real-time security metrics
- Risk level indicator
- Interactive charts
- Search & filter events
- Event severity classification

### 🔍 Investigation Workflow
- Clickable security events
- Event details page
- Investigation status management
- Analyst notes
- Security event tracking

### 📁 Audit Logging
- SQLite-based event logging
- Timestamped security events
- CSV export support
- Searchable audit logs

---

# 🏗️ System Architecture

```text
                 User
                   │
                   ▼
      ┌─────────────────────────┐
      │ FastAPI Security Gateway│
      └─────────────────────────┘
                   │
      ┌────────────┼─────────────┐
      │            │             │
      ▼            ▼             ▼
 API Key     Prompt Injection   PII
 Validator       Filter       Detection
      │            │             │
      └────────────┼─────────────┘
                   ▼
          Response Filter
                   │
                   ▼
         SQLite Audit Logging
                   │
                   ▼
      Security Monitoring Dashboard
```

---

# 🧩 Modules

## Authentication Module
- JWT Authentication
- User Verification
- Role Validation

## API Key Validator
- Incoming request validation
- Unauthorized API detection

## Prompt Injection Filter
- Detects malicious prompts
- Prevents prompt manipulation attacks

## PII Detection Module
- Detects sensitive personal information
- Protects confidential user data

## Response Filter
- Prevents sensitive information disclosure
- Blocks restricted AI responses

## Dashboard Module
- Security analytics
- Event monitoring
- Investigation workflow
- Risk visualization

## Database Module
- SQLite storage
- Audit logging
- Event retrieval

---

# 📂 Project Structure

```text
Enterprise-LLM-Security-Gateway/

├── app/
│   ├── api_key_validator.py
│   ├── auth.py
│   ├── auth_middleware.py
│   ├── dashboard.py
│   ├── database.py
│   ├── deanonymizer.py
│   ├── prompt_filter.py
│   ├── response_filter.py
│   └── main.py
│
├── tests/
├── .github/
├── gateway.db
├── requirements.txt
├── README.md
└── .gitignore
```

---

# 💻 Technology Stack

| Technology | Purpose |
|------------|---------|
| Python | Backend Development |
| FastAPI | REST API Framework |
| SQLite | Audit Logging Database |
| HTML | Dashboard Interface |
| CSS | Styling |
| JavaScript | Dashboard Functionality |
| Chart.js | Security Analytics |
| JWT | Authentication |
| Git | Version Control |
| GitHub | Source Code Hosting |

---

# 🚀 Installation

## Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/Enterprise-LLM-Security-Gateway.git
```

## Navigate to Project

```bash
cd Enterprise-LLM-Security-Gateway
```

## Create Virtual Environment

```bash
python -m venv .venv
```

## Activate Virtual Environment

### Windows

```bash
.venv\Scripts\activate
```

### Linux / macOS

```bash
source .venv/bin/activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Run Application

```bash
uvicorn app.main:app --reload
```

---

# 🌐 Application URLs

| Service | URL |
|----------|-----|
| API | http://127.0.0.1:8000 |
| Dashboard | http://127.0.0.1:8000/dashboard |
| Swagger UI | http://127.0.0.1:8000/docs |

---

# 📊 Dashboard Capabilities

- Security Metrics
- Risk Level Indicator
- Event Analytics
- Search Events
- Filter Events
- Severity Labels
- Event Investigation
- Analyst Notes
- CSV Export

---

# 🔐 Security Events Monitored

- API Key Violations
- Prompt Injection Attempts
- PII Detection
- Sensitive Response Blocking

---

# 📸 Screenshots

## Dashboard

![Dashboard](docs/screenshots/dashboard.png)

---

## Analytics Chart

![Analytics](docs/screenshots/analytics_chart.png)

---

## Security Events

![Security Events](docs/screenshots/security_events.png)

---

## Event Investigation

![Event Investigation](docs/screenshots/event_investigation.png)

---

## Investigation Workflow

![Investigation Workflow](docs/screenshots/investigation_workflow.png)

# 🧪 Testing

The application was tested for the following scenarios:

- API Key Validation
- Prompt Injection Detection
- PII Detection
- Response Filtering
- Dashboard Monitoring
- Event Investigation
- CSV Export

---

# 🔮 Future Enhancements

- PostgreSQL Integration
- Docker Support
- Kubernetes Deployment
- SIEM Integration
- Email Alerts
- Elasticsearch Logging
- Real-Time Monitoring
- Multi-Factor Authentication (MFA)
- AI-based Threat Scoring

---

# 👨‍💻 Author

**Muhammed Wazeem**

Bachelor of Computer Applications (Cybersecurity, Ethical Hacking & Cloud Computing)

Internship Project

Enterprise LLM & GenAI Security Gateway

---

# 📄 License

This project was developed for educational and internship purposes.