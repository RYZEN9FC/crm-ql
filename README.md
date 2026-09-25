# QuantumLoop CRM

A lightweight CRM (Customer Relationship Management) application developed using **Flask** and **SQLite**, designed for managing leads, telecalling operations, customer interactions, and internal business workflows.

---

## Features

* Lead Management
* Customer Database
* Telecaller Workflow
<<<<<<< HEAD
=======
* Field Sales Visits & Daily Work Sessions
>>>>>>> b90a4fe (Update CRM invoice and field visit modules)
* Lead Assignment & Transfers
* Reports & Exports (Excel)
* PDF Generation
* Authentication & Session Management
* Role-Based Access
* Secure Environment-Based Configuration

---

## Technology Stack

* **Backend:** Python, Flask
* **Database:** SQLite
* **Frontend:** HTML, CSS, JavaScript
* **Excel Processing:** OpenPyXL
* **PDF Generation:** ReportLab
* **Environment Variables:** python-dotenv

---

## Requirements

* Python 3.10+
* pip
* Virtual Environment (recommended)

---

## Installation

### Clone Repository

```bash
git clone https://github.com/RYZEN9FC/crm-ql.git
cd crm-ql
```

### Create Virtual Environment

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Configuration

Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key
SESSION_COOKIE_SECURE=false
<<<<<<< HEAD
=======
FIELD_PHOTO_DIR=/secure/persistent/path/field_visit_photos
>>>>>>> b90a4fe (Update CRM invoice and field visit modules)
```

Example file:

```text
.env.example
```

**Important:**

* `.env` should never be committed to Git.
* Production secrets are stored separately on the server.
<<<<<<< HEAD
=======
* `FIELD_PHOTO_DIR` is optional. When omitted, protected visit photos are stored under Flask's local `instance/field_visit_photos` directory. Back this directory up in production.

---

## Field Sales Workflow

Managers can schedule visits against an existing lead or company and assign them to a Field Sales Executive. Executives can also create independent visits, or create a duplicate-checked lead before starting a visit.

Executives start one daily field-work session, check in with a location status, capture office and visiting-card evidence directly from the device camera, submit visit outcomes and next actions, and end field work after the last visit. Unclosed sessions reconcile to a system-assumed 6:30 p.m. IST end time. Managers can accept visits or return them with a correction comment.
>>>>>>> b90a4fe (Update CRM invoice and field visit modules)

---

## Running Locally

```bash
python app.py
```

Application will be available at:

```text
http://127.0.0.1:5000
```

---

## Production Deployment

Production deployment is automated using:

* GitHub Actions
* SSH Deployment
* Gunicorn
* Nginx
* Environment Variables

Production secrets are stored in:

```text
/etc/quantumloop-crm.env
```

---

## Security

* Environment-based `SECRET_KEY`
* HTTPOnly Session Cookies
* SameSite Cookie Protection
* Secure Cookies in Production
* Secrets excluded from Git

---

## Project Structure

```text
crm-ql/
│
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
├── templates/
├── static/
├── leads.db
├── invoice_pdf.py
├── uploads/
└── README.md
```

---

## License

Internal Project – QuantumLoop Pvt. Ltd.

---

## Developed By

QuantumLoop Pvt. Ltd.
Hyderabad, Telangana, India
