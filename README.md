# OpenLib - Library Management System

**OpenLib** is a Django-based web application designed for managing library operations. It provides role-based access for both administrators and general users, featuring user authentication, email subscriptions, a contact system, and dedicated portals for user interaction and administration.

---

## 🚀 Features

- **Role-Based Access Control (RBAC)**: Distinct workflows and dashboards for **Admin** and **User** roles.
- **Authentication System**: User signup, login, role selection, and user management.
- **Main Content Portal**:
  - Landing page (`Home`)
  - Info & About section (`About`) with integrated newsletter subscription forms
  - Contact Us system (`Contact`) with automatic email confirmation and notification routing
- **User Portal (`userpage`)**: Dedicated interface for library users.
- **Admin Panel (`adminpanel`)**: Comprehensive administrative interface for library management.
- **Developer Toolbar**: Pre-configured with `django-debug-toolbar` for debugging and performance profiling during development.

---

## 🛠️ Tech Stack

- **Backend**: Python 3.x, Django 4.2+
- **Database**: SQLite3 (default development database)
- **Frontend**: HTML5, CSS3, JavaScript, Django Templates
- **Tools & Utilities**: Django Debug Toolbar, `django.core.mail` for email notifications

---

## 📁 Project Structure

```text
OpenLib/
│── Openlib/             # Project Configuration (settings, root URLs, WSGI/ASGI)
│   ├── settings.py
│   ├── urls.py
│   └── info.py          # Email configuration file (credentials)
│
│── maincontent/         # Home, About, Contact pages & Subscription models
│   ├── templates/
│   ├── forms.py
│   ├── models.py
│   └── views.py
│
│── signup/              # Authentication & Registration (CustomUser model)
│   ├── templates/
│   ├── forms.py
│   ├── models.py
│   └── views.py
│
│── adminpanel/          # Admin Dashboard & Management Views
│   ├── templates/
│   └── views.py
│
│── userpage/            # User Dashboard & Portal Views
│   ├── templates/
│   └── views.py
│
│── static/              # Static assets (CSS, JS, Images)
│── staticfiles/         # Collected static files (for production)
│── db.sqlite3           # SQLite Database file
│── manage.py            # Django management script
└── README.md            # Project documentation
```

---

## ⚙️ Installation & Setup

### Prerequisites

- Python 3.8+ installed on your system
- `pip` (Python package manager)

### 1. Clone the Repository

```bash
git clone https://github.com/Faiz-Shaikh-001/OpenLib.git
cd OpenLib
```

### 2. Create and Activate a Virtual Environment

- **On Windows (PowerShell):**
  ```powershell
  python -m venv venv
  .\venv\Scripts\Activate.ps1
  ```

- **On macOS/Linux:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

### 3. Install Dependencies

```bash
pip install django django-debug-toolbar
```

### 4. Configure Email Credentials (Optional)

Create or update the file `Openlib/info.py` with your SMTP settings for email support:

```python
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
EMAIL_PORT = 587
```

### 5. Apply Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create a Superuser (Admin)

```bash
python manage.py createsuperuser
```

---

## 🏃 Running the Server

Start the Django development server:

```bash
python manage.py runserver
```

Open your browser and navigate to:
- **Application Home**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Signup / Login**: [http://127.0.0.1:8000/signup/](http://127.0.0.1:8000/signup/)
- **Django Admin**: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
- **Admin Panel**: [http://127.0.0.1:8000/adminpage/](http://127.0.0.1:8000/adminpage/)
- **User Page**: [http://127.0.0.1:8000/userpage/](http://127.0.0.1:8000/userpage/)

---

## 📄 License

This project is open-source under the MIT License.
