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

🧪 Testing Workflow
Step-by-step testing instructions for the API:

Register a new user
POST /api/auth/register/
Use the registration payload to create a new user account.
Login with the registered user
POST /api/auth/login/
Use the email and password to receive JWT access and refresh tokens.
Create a patient
POST /api/patients/
Provide patient data and include the access token in the Authorization header.
Create a doctor
POST /api/doctors/
Provide doctor details and include the access token.
Assign a doctor to a patient
POST /api/mappings/
Use patient ID and doctor ID to create the mapping.
Test GET endpoints
Retrieve all patients: GET /api/patients/
Retrieve specific patient: GET /api/patients/{id}/
Retrieve all doctors: GET /api/doctors/
Retrieve mappings: GET /api/mappings/
Get doctors assigned to a patient: GET /api/mappings/patient/{patient_id}/
Test UPDATE endpoints
Update patient: PUT /api/patients/{id}/
Update doctor: PUT /api/doctors/{id}/
Test DELETE endpoints
Delete patient: DELETE /api/patients/{id}/
Delete doctor: DELETE /api/doctors/{id}/
Remove patient-doctor mapping: DELETE /api/mappings/{mapping_id}/

Sample Patient:
{
  "name": "Alice Johnson",
  "email": "alice.johnson@email.com",
  "phone": "+1555123456",
  "age": 28,
  "gender": "F",
  "address": "789 Oak Ave, Springfield, IL 62701",
}

Sample Doctor:
{
  "name": "Dr. Sarah Wilson",
  "email": "sarah.wilson@medcenter.com",
  "phone": "+1555789012",
  "specialization": "PEDIATRICS",
  "license_number": "MD98765",
  "years_of_experience": 12,
  "consultation_fee": "120.00"
}




