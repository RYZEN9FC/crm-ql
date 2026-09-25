# Google Authentication Setup — QuantumLoop CRM

This guide configures the CRM for Google-only login. Password login has been removed. A Google account must be authorized in the CRM before it can sign in.

## 1. Install the project dependencies

Open PowerShell inside the `crm-ql` directory and run:

```powershell
python -m pip install -r requirements.txt
```

## 2. Create a Google Cloud project

1. Open [Google Cloud Console](https://console.cloud.google.com/).
2. Click the project selector at the top.
3. Select **New Project**.
4. Enter `QuantumLoop CRM` as the project name.
5. Click **Create**.
6. Make sure the new project is selected.

## 3. Configure the Google consent screen

1. Open [Google Auth Platform](https://console.cloud.google.com/auth/overview).
2. Click **Get started** if requested.
3. Under **Branding**, enter:

   - App name: `QuantumLoop CRM`
   - User support email: your company email
   - Developer contact email: your company email

4. Save the configuration.

The CRM requests only the standard `openid`, `email`, and `profile` identity scopes. It does not request access to Gmail, Drive, or Calendar.

## 4. Configure the audience

Open **Google Auth Platform → Audience** and choose one of the following:

- **Internal** — use this when everybody signs in with Google Workspace accounts from the same company organization.
- **External** — use this when employees use normal Gmail accounts or accounts from different organizations.

If the app is **External** and remains in testing mode:

1. Find **Test users**.
2. Add the manager's Google email.
3. Add every telecaller, Field Sales Executive, and manager who needs to test the CRM.

Testing projects are limited to the users listed in the Google consent-screen configuration. See [Google's audience documentation](https://support.google.com/cloud/answer/15549945) for the current restrictions.

## 5. Create the OAuth client

1. Open **Google Auth Platform → Clients**.
2. Click **Create Client**.
3. Select **Web application**.
4. Enter `QuantumLoop CRM Web` as the name.
5. Under **Authorized redirect URIs**, add:

```text
http://127.0.0.1:5000/auth/google/callback
```

If the application will be opened using `localhost`, optionally add:

```text
http://localhost:5000/auth/google/callback
```

For production, add the real HTTPS callback:

```text
https://your-crm-domain.com/auth/google/callback
```

The redirect URI must match exactly, including the scheme, hostname, port, path, and trailing slash. Otherwise, Google returns `redirect_uri_mismatch`. See [Google's OAuth web-server documentation](https://developers.google.com/identity/protocols/oauth2/web-server).

6. Click **Create**.
7. Immediately copy the **Client ID** and **Client secret**.

Keep the client secret private and never commit it to Git. Google may only display or allow downloading the secret when the client is created.

## 6. Configure the local `.env` file

Open `.env` in the project root. Keep the existing `SECRET_KEY` and add:

```env
SESSION_COOKIE_SECURE=false

GOOGLE_CLIENT_ID=PASTE_YOUR_CLIENT_ID_HERE
GOOGLE_CLIENT_SECRET=PASTE_YOUR_CLIENT_SECRET_HERE
GOOGLE_REDIRECT_URI=http://127.0.0.1:5000/auth/google/callback

GOOGLE_BOOTSTRAP_EMAILS=manager@gmail.com
GOOGLE_ALLOWED_DOMAIN=
LOGIN_SESSION_DAYS=3650
TRUST_PROXY_HEADERS=false
```

Replace `manager@gmail.com` with the Google email of the first CRM manager.

Do not add quotation marks around environment-variable values.

```env
# Correct
GOOGLE_CLIENT_ID=123456.apps.googleusercontent.com

# Incorrect
GOOGLE_CLIENT_ID="123456.apps.googleusercontent.com"
```

### Optional company-domain restriction

To accept only accounts from one Google Workspace domain, set:

```env
GOOGLE_ALLOWED_DOMAIN=yourcompany.com
```

Leave it empty when employees use Gmail or multiple domains:

```env
GOOGLE_ALLOWED_DOMAIN=
```

## 7. Link the first existing manager

The existing database may contain manager accounts created with usernames and passwords. Use the bootstrap setting to link the first manager safely.

1. Set the manager's actual Google email:

```env
GOOGLE_BOOTSTRAP_EMAILS=manager@gmail.com
```

2. Start the application:

```powershell
python app.py
```

3. Open:

```text
http://127.0.0.1:5000/login
```

4. Click **Continue with Google**.
5. Select the same email entered in `GOOGLE_BOOTSTRAP_EMAILS`.
6. Complete Google's consent screen.
7. Google will return to the CRM and link that account to the first existing manager without an email.

After the manager logs in successfully, remove the bootstrap access:

```env
GOOGLE_BOOTSTRAP_EMAILS=
```

Restart the application after changing `.env`.

## 8. Authorize the other CRM users

Log in as a manager and open **Users**.

For every existing user:

1. Find the user.
2. Enter their exact Google email.
3. Click **Save**.
4. The status will show **Ready for first login**.
5. After the employee logs in, the status will show **Google linked**.

To add a new user:

1. Enter their name.
2. Enter their Google email.
3. Select their role:
   - Telecaller
   - Field Sales Executive
   - Customer Relations Manager
4. Click **Add user**.

An email must be authorized from the Users page before that person can access the CRM.

## 9. Test persistent login

1. Log in using Google.
2. Close the browser completely.
3. Reopen the browser.
4. Visit `http://127.0.0.1:5000`.

The CRM should open without requesting Google login again.

The user will need to sign in again if:

- They click **Logout**.
- Browser cookies are cleared.
- They use an incognito/private window.
- The server's `SECRET_KEY` changes.
- The configured session duration expires.

The default `LOGIN_SESSION_DAYS=3650` is ten years and is refreshed as the CRM is used.

## 10. Production configuration

Use the following values on the production server:

```env
SESSION_COOKIE_SECURE=true
GOOGLE_CLIENT_ID=your-production-client-id
GOOGLE_CLIENT_SECRET=your-production-client-secret
GOOGLE_REDIRECT_URI=https://crm.yourdomain.com/auth/google/callback
GOOGLE_BOOTSTRAP_EMAILS=
LOGIN_SESSION_DAYS=3650
```

If Nginx is the trusted reverse proxy directly in front of Flask or Gunicorn, also set:

```env
TRUST_PROXY_HEADERS=true
```

Then:

1. Add the exact production callback URI to the OAuth client in Google Cloud.
2. Confirm the production domain uses HTTPS.
3. Install the updated requirements on the server.
4. Keep the production `SECRET_KEY` stable.
5. Restart the application service.
6. Test login in a private browser window.

## Troubleshooting

### `redirect_uri_mismatch`

The value in `GOOGLE_REDIRECT_URI` and the URI registered in Google Cloud are not identical. Check:

- `http` versus `https`
- `127.0.0.1` versus `localhost`
- Port `5000`
- `/auth/google/callback`
- Trailing slash differences

### Google account is not authorized

- Add the email from the manager's **Users** page.
- For the first existing manager, set `GOOGLE_BOOTSTRAP_EMAILS`.
- If Google OAuth is in testing mode, also add the account under Google's **Test users**.

### Login does not stay active locally

- Confirm `SESSION_COOKIE_SECURE=false` for local HTTP.
- Do not use an incognito/private window.
- Do not change `SECRET_KEY` between restarts.
- Check whether the browser blocks or clears cookies.

### Google login is not configured

- Check `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET` in `.env`.
- Make sure there are no quotation marks or extra spaces.
- Restart `python app.py` after editing `.env`.
- Run `python -m pip install -r requirements.txt`.

### Google shows “Access blocked”

- Add the account under **Test users** when the app is in testing mode.
- Check whether a Google Workspace administrator blocks third-party applications.
- Verify that the OAuth client belongs to the selected Google Cloud project.

## Security reminders

- Never commit `.env` or the Google client secret.
- Use HTTPS and `SESSION_COOKIE_SECURE=true` in production.
- Remove `GOOGLE_BOOTSTRAP_EMAILS` after the first manager is linked.
- Restrict `GOOGLE_ALLOWED_DOMAIN` when all employees use one Workspace domain.
- Keep `SECRET_KEY` stable and private.
- Remove CRM access immediately when an employee leaves the company.

