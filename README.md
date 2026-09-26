# QuantumLoop CRM

A lightweight CRM (Customer Relationship Management) application developed using **Flask** and **SQLite**, designed for managing leads, telecalling operations, customer interactions, and internal business workflows.

---

## Features

* Lead Management
* Customer Database
* Telecaller Workflow
* Field Sales Visits & Daily Work Sessions
* Lead Assignment & Transfers
* Reports & Exports (Excel)
* PDF Generation
* Authentication & Session Management
* Role-Based Access
* Secure Environment-Based Configuration

---

## Technology Stack

* **Backend:** Python, Flask
* **Authentication:** Google OpenID Connect (Authlib)
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
GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-client-secret
GOOGLE_REDIRECT_URI=http://127.0.0.1:5000/auth/google/callback
GOOGLE_BOOTSTRAP_EMAILS=manager@yourcompany.com
FIELD_PHOTO_DIR=/secure/persistent/path/field_visit_photos
```

Example file:

```text
.env.example
```

**Important:**

* `.env` should never be committed to Git.
* Production secrets are stored separately on the server.
* `FIELD_PHOTO_DIR` is optional. When omitted, protected visit photos are stored under Flask's local `instance/field_visit_photos` directory. Back this directory up in production.

### Google Login Setup

1. In Google Cloud Console, create an OAuth 2.0 Client ID with application type **Web application**.
2. Add `http://127.0.0.1:5000/auth/google/callback` as an authorized redirect URI for local development. Add the exact HTTPS callback URL for production, such as `https://crm.example.com/auth/google/callback`.
3. Copy the client ID, client secret and exact redirect URI into `.env`.
4. For an existing database, set `GOOGLE_BOOTSTRAP_EMAILS` to the first manager's Google email. That address may bind the first manager account that does not yet have an email. Remove the bootstrap value after the manager has logged in.
5. From the manager's **Users** page, assign the correct Google email to every telecaller, Field Sales Executive and manager.

Password login is disabled. Google must return a verified email that is already authorized in the CRM. A successful login creates a persistent CRM session (10 years by default, refreshed with use) so the same browser stays signed in until logout, cookie removal or a server secret change. Change `LOGIN_SESSION_DAYS` if a shorter policy is required.

### Manual Manager Recovery Login

If the first manager cannot use Google yet because no CRM emails have been assigned, temporarily enable the manager-only fallback:

```env
MANUAL_ADMIN_LOGIN_ENABLED=true
```

Existing managers created before Google login can use their original manager username and password at `/admin-login`. Alternatively, generate a recovery password hash:

```powershell
python -c "from getpass import getpass; from werkzeug.security import generate_password_hash; print(generate_password_hash(getpass('New manual admin password: ')))"
```

Then configure the server without storing the plain password:

```env
MANUAL_ADMIN_USERNAME=admin
MANUAL_ADMIN_PASSWORD_HASH=paste-the-generated-hash-here
```

Restart the app, open `/admin-login`, sign in, and assign each user's Google email from **Users**. The fallback accepts manager access only and blocks attempts for 15 minutes after five failures. Set `MANUAL_ADMIN_LOGIN_ENABLED=false` and restart after recovery is complete.

---

## Field Sales Workflow

Managers can schedule visits against an existing lead or company and assign them to a Field Sales Executive. Executives can also create independent visits, or create a duplicate-checked lead before starting a visit.

Executives start one daily field-work session, check in with a location status, capture office and visiting-card evidence directly from the device camera, submit visit outcomes and next actions, and end field work after the last visit. Unclosed sessions reconcile to a system-assumed 6:30 p.m. IST end time. Managers can accept visits or return them with a correction comment.

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
