# 🏥 Django Healthcare Backend - Setup Guide

A full-featured REST API for managing patients, doctors, and their mappings using Django, PostgreSQL, and JWT Authentication.

---

## 🚀 Quick Setup Instructions

### 1. Prerequisites
- Python 3.8+
- PostgreSQL installed and running
- Postman or any API testing tool

---

### 2. Project Setup

```bash
# Create project directory
mkdir healthcare_project
cd healthcare_project

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create PostgreSQL database
createdb healthcare_db

# Or using PostgreSQL CLI:
psql -U postgres
CREATE DATABASE healthcare_db;
\q

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser (optional, for admin access)
python manage.py createsuperuser

# Run the development server
python manage.py runserver

healthcare_project/
├── healthcare_project/
│   ├── settings.py
│   ├── urls.py
│   └── ...
├── healthcare_api/
│   ├── models.py
│   ├── serializers.py
│   ├── urls.py
│   └── views.py
├── .env
├── manage.py
└── requirements.txt

