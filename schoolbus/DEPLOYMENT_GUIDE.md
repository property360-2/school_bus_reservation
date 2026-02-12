# Deploying to PythonAnywhere: Step-by-Step Guide

This guide will walk you through deploying your Django project (`schoolbus`) to PythonAnywhere.

## Prerequisites
1.  A [PythonAnywhere](https://www.pythonanywhere.com/) account (Basic/Free is fine).
2.  Your project files ready.

---

## Step 1: Prepare Your Project Locally

Before uploading, we need to make a few small adjustments to your `settings.py` to make it production-ready.

1.  **Open `schoolbus/schoolbus/settings.py`** and modify/add these lines:

    ```python
    import os

    # SECURITY: Change this to False for production, but keep True for now to debug errors
    DEBUG = True  # You can switch to False once everything works

    # ALLOWED_HOSTS: Add your PythonAnywhere domain here
    # Replace 'yourusername' with your actual PythonAnywhere username
    ALLOWED_HOSTS = ['yourusername.pythonanywhere.com', 'localhost', '127.0.0.1']

    # STATIC FILES: Add this line at the bottom of the file
    # This tells Django where to collect all static files (CSS, images)
    STATIC_ROOT = BASE_DIR / "staticfiles"
    ```

2.  **Generate `requirements.txt`**:
    We have already created a basic `requirements.txt` for you. It contains:
    ```text
    Django>=4.0
    python-dotenv
    whitenoise
    ```

---

## Step 2: Upload Your Project to PythonAnywhere

1.  **Log in** to your PythonAnywhere dashboard.
2.  Go to the **"Files"** tab.
3.  You can upload your files in two ways:
    *   **Option A (Easy for Beginners):** Zip your entire `schoolbus` folder, upload the zip file, and run `unzip schoolbus.zip` in a Bash console.
    *   **Option B (Better):** If you use GitHub, open a **Bash Console** and clone your repo:
        ```bash
        git clone https://github.com/yourusername/your-repo.git
        ```

    *For this guide, we assume your code is at `/home/yourusername/schoolbus`.*

---

## Step 3: Set Up Virtual Environment

1.  Open a **Bash Console** from your Dashboard.
2.  Navigate to your project folder:
    ```bash
    cd schoolbus
    ```
3.  Create a virtual environment:
    ```bash
    mkvirtualenv --python=/usr/bin/python3.10 mysite-virtualenv
    ```
    *(Note: You can choose Python 3.8, 3.9, or 3.10. Just make sure it matches what you set in the Web tab later.)*
4.  Your prompt should now change to `(mysite-virtualenv) ...`.
5.  Install your dependencies:
    ```bash
    pip install -r requirements.txt
    ```

---

## Step 4: Configure the Web App

1.  Go to the **"Web"** tab in PythonAnywhere.
2.  Click **"Add a new web app"**.
3.  **Domain:** Confirm your domain (e.g., `yourusername.pythonanywhere.com`).
4.  **Framework:** Select **"Manual configuration"** (NOT Django, as "Manual" gives you more control and is often less error-prone for existing projects).
5.  **Python Version:** Select **Python 3.10** (or whatever version you used in the virtualenv).
6.  Click **Next**.

### configure WSGI File
1.  In the **"Code"** section of the Web tab, look for **"WSGI configuration file"**.
2.  Click the link to edit it.
3.  Delete **everything** in that file and paste this:

    ```python
    import os
    import sys

    # path to your project folder
    path = '/home/yourusername/schoolbus'
    if path not in sys.path:
        sys.path.append(path)

    # set environment variable to tell django where your settings.py is
    os.environ['DJANGO_SETTINGS_MODULE'] = 'schoolbus.settings'

    # activate your virtualenv
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
    ```
    *(**Important:** Replace `yourusername` with your actual PythonAnywhere username!)*
4.  Click **Save**.

### Configure Virtual Environment Path
1.  Back in the **Web** tab, look for the **"Virtualenv"** section.
2.  Enter the path to your virtual environment:
    ```
    /home/yourusername/.virtualenvs/mysite-virtualenv
    ```
    *(Replace `yourusername`!)*

---

## Step 5: Database and Static Files

1.  Go back to your **Bash Console**.
2.  Run database migrations (to set up SQLite):
    ```bash
    python manage.py migrate
    ```
3.  Collect static files (CSS/Images):
    ```bash
    python manage.py collectstatic
    ```
    *(Type `yes` if asked to overwrite).*

---

## Step 6: Static Files Configuration (Web Tab)

This ensures your CSS and images load correctly.

1.  Go to the **"Web"** tab.
2.  Scroll down to **"Static files"**.
3.  Click **"Enter URL"** and type: `/static/`
4.  Click **"Enter path"** and type: `/home/yourusername/schoolbus/staticfiles`
    *(Note: This must match the `STATIC_ROOT` path we set in Step 1. Wait, did we set it to `staticfiles` or `static`? Check your `settings.py`. Based on this guide, use `staticfiles`.)*

---

## Step 7: Launch!

1.  Go to the top of the **"Web"** tab.
2.  Click the big green **"Reload"** button.
3.  Click the link to your site (`yourusername.pythonanywhere.com`).

---

## Troubleshooting Common Errors

### "DisallowedHost" / "Bad Request (400)"
*   **Fix:** Checked `ALLOWED_HOSTS` in `settings.py`. It MUST include your specific PythonAnywhere domain.

### "ModuleNotFoundError: No module named 'django'"
*   **Fix:** Ensure your **Virtualenv path** in the Web tab is correct. It typically looks like `/home/yourusername/.virtualenvs/mysite-virtualenv`.

### CSS/Styles Missing (Ugly Page)
*   **Fix:** Double-check the **Static Files** section in the Web tab.
    *   URL: `/static/`
    *   Path: `/home/yourusername/schoolbus/staticfiles`
    *   Did you run `python manage.py collectstatic`?

### Database Errors (OperationalError)
*   **Fix:** Did you run `python manage.py migrate`? Ensure the `db.sqlite3` file is in the project folder.
