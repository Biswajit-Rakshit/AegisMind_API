# AegisMind API

AegisMind API is a secure employee sentiment analytics platform built with Django REST Framework (DRF). The system enables employees to submit anonymous feedback while ensuring privacy through k-anonymity based analytics and role-based access controls.

The project is designed with enterprise-grade principles in mind, focusing on data privacy, access restrictions, authentication, and secure analytics reporting.

---

## Features

### Authentication & Authorization

* JWT-based authentication
* Custom User Model
* Role-based access control
* Custom permission classes
* Admin-controlled user provisioning

### Survey Management

* Employees can submit anonymous survey responses
* Survey responses cannot be retrieved directly through public APIs
* Business rules enforced through API permissions

### Privacy & Analytics

* Department-level analytics
* 5-Anonymity (k-anonymity) enforcement
* Analytics are displayed only when a department has at least 5 survey responses
* Privacy-first data aggregation

### API Security

* Custom DRF Throttling
* One survey submission per employee per week
* Access restrictions based on user roles

### Testing

* Unit tests for Accounts APIs
* Unit tests for Survey APIs
* Unit tests for Analytics APIs
* Business-rule validation testing

### API Documentation

* Interactive Swagger/OpenAPI Documentation
* Auto-generated API schemas using drf-spectacular

### Enterprise-Oriented Design

* Organization email generation using configurable domain
* Environment-based configuration
* Separation of employee and administrator responsibilities
* Secure API design

---

## Tech Stack

* Python
* Django
* Django REST Framework (DRF)
* JWT Authentication
* PostgreSQL
* drf-spectacular (Swagger/OpenAPI)
* Git & GitHub

---

## Project Structure

```text
AegisMind_API/
│
├── accounts/
├── analytics/
├── surveys/
│
├── manage.py
├── requirements.txt
└── README.md
```

---

## Key Business Rules

### User Management

* Employees cannot self-register
* Only administrators can create employee accounts

### Survey Submission

* Employees can submit only one survey per week
* Survey responses remain anonymous

### Analytics Privacy

* Analytics are displayed only when a minimum of 5 responses exist within a group
* Prevents individual employee identification

---

## Environment Variables

Create a `.env` file in the project root.

```env
# Django settings
SECRET_KEY=your-secret-key
DEBUG=your-debug-setting
ALLOWED_HOSTS=your-allowed-hosts-comma-separated

# Database configuration
DB_NAME=your-db-name
DB_USER=your-db-user
DB_PASSWORD=your-db-password
DB_HOST=your-host
DB_PORT=your-port

# Organisation details
ORG_NAME=your-org-name
ORG_DOMAIN=your-org-domain
```

---

## Installation

### Clone Repository

```bash
git clone https://github.com/Biswajit-Rakshit/AegisMind_API.git
cd AegisMind_API
```

### Create Virtual Environment

```bash
python -m venv venv
```

Activate virtual environment:

```bash
source venv/bin/activate
```

or on Windows:

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Run Server

```bash
python manage.py runserver
```

---

## Testing

The project includes automated test coverage for:

* User Registration
* Authentication
* Permissions
* Survey Submission
* Analytics APIs
* Privacy Enforcement Rules
* Throttling Rules

Run tests:

```bash
python manage.py test
```

---

## API Documentation

Swagger UI is available after running the server:

```text
/api/schema/swagger-ui/
```

OpenAPI schema:

```text
/api/schema/
```

---

## Design Decisions

### Why k-Anonymity?

Employee sentiment data is highly sensitive. To preserve anonymity and reduce the risk of identifying individual employees, analytics are only exposed when a minimum threshold of five responses exists within a department.

### Why Admin-Controlled User Creation?

In most enterprise environments, employees do not self-register. User provisioning is typically managed by HR, IT, or system administrators. The project reflects this real-world workflow.

### Why Restrict Survey Retrieval?

The platform is designed to collect anonymous feedback. Allowing unrestricted access to survey responses could compromise employee privacy. Therefore, analytics are exposed through aggregated reports rather than individual response retrieval.

---

## Current Status

✅ Authentication Implemented

✅ Role-Based Access Control

✅ Survey Management APIs

✅ K-Anonymity Analytics

✅ Weekly Submission Restriction

✅ Automated Testing

✅ Swagger Documentation

🚧 Weekly Analytics Filtering (In Progress)

---

## Future Improvements

* Weekly Analytics Filtering
* Docker Support
* AWS Deployment
* CI/CD Pipeline
* Advanced Reporting & Dashboards

---

## Author

### Biswajit Rakshit

Associate Analyst | Deloitte USI

Currently focused on Django, Django REST Framework, API Design, and Backend Engineering
