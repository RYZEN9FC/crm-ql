# QuantumLoop CRM

A lightweight CRM (Customer Relationship Management) application developed using **Flask** and **SQLite**, designed for managing leads, telecalling operations, customer interactions, and internal business workflows.

---

## Features

* Lead Management
* Customer Database
* Telecaller Workflow
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
```

Example file:

```text
.env.example
```

**Important:**

* `.env` should never be committed to Git.
* Production secrets are stored separately on the server.

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
