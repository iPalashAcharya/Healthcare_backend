Django Healthcare Backend - Setup & Testing Guide
🚀 Quick Setup Instructions
1. Prerequisites

Python 3.8+ installed
PostgreSQL installed and running
Postman or any API testing tool

2. Project Setup
bash# Create project directory
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
3. Database Setup
bash# Create PostgreSQL database
createdb healthcare_db

# Or using PostgreSQL command line:
psql -U postgres
CREATE DATABASE healthcare_db;
\q
4. Django Setup
bash# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser (optional, for admin access)
python manage.py createsuperuser

# Run the development server
python manage.py runserver
📁 Project Structure
healthcare_project/
├── healthcare_project/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── healthcare_api/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── urls.py
│   └── views.py
├── .env
├── manage.py
└── requirements.txt

🔧 API Testing Guide
Base URL: http://localhost:8000/api/

1. Authentication APIs
Register User
httpPOST /api/auth/register/
Content-Type: application/json

{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "password": "securepassword123",
    "password_confirm": "securepassword123"
}
Response:
json{
    "message": "User registered successfully",
    "user": {
        "id": 1,
        "name": "John Doe",
        "email": "john.doe@example.com"
    },
    "tokens": {
        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
        "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
    }
}

Login User
httpPOST /api/auth/login/
Content-Type: application/json

{
    "email": "john.doe@example.com",
    "password": "securepassword123"
}

2. Patient Management APIs
Note: All patient APIs require authentication. Add header:
Authorization: Bearer YOUR_ACCESS_TOKEN
Create Patient
httpPOST /api/patients/
Content-Type: application/json
Authorization: Bearer YOUR_ACCESS_TOKEN

{
    "name": "Jane Smith",
    "email": "jane.smith@example.com",
    "phone": "+1234567890",
    "age": 30,
    "gender": "F",
    "address": "123 Main St, City, State 12345"
}

Get All Patients
httpGET /api/patients/
Authorization: Bearer YOUR_ACCESS_TOKEN

Get Specific Patient
httpGET /api/patients/1/
Authorization: Bearer YOUR_ACCESS_TOKEN

Update Patient
httpPUT /api/patients/1/
Content-Type: application/json
Authorization: Bearer YOUR_ACCESS_TOKEN

{
    "name": "Jane Smith Updated",
    "email": "jane.smith@example.com",
    "phone": "+1234567890",
    "age": 31,
    "gender": "F",
    "address": "456 New St, City, State 12345"
}

Delete Patient
httpDELETE /api/patients/1/
Authorization: Bearer YOUR_ACCESS_TOKEN

3. Doctor Management APIs
Create Doctor
httpPOST /api/doctors/
Content-Type: application/json
Authorization: Bearer YOUR_ACCESS_TOKEN

{
    "name": "Dr. Michael Johnson",
    "email": "michael.johnson@hospital.com",
    "phone": "+1122334455",
    "specialization": "CARDIOLOGY",
    "license_number": "MD12345",
    "years_of_experience": 15,
    "consultation_fee": "150.00"
}

Get All Doctors
httpGET /api/doctors/
Authorization: Bearer YOUR_ACCESS_TOKEN

Get Specific Doctor
httpGET /api/doctors/1/
Authorization: Bearer YOUR_ACCESS_TOKEN

Update Doctor
httpPUT /api/doctors/1/
Content-Type: application/json
Authorization: Bearer YOUR_ACCESS_TOKEN

{
    "name": "Dr. Michael Johnson Updated",
    "email": "michael.johnson@hospital.com",
    "phone": "+1122334455",
    "speciality": "NEUROLOGY",
    "license_number": "MD12345",
    "years_of_experience": 16,
    "consultation_fee": "175.00"
}

Delete Doctor
httpDELETE /api/doctors/1/
Authorization: Bearer YOUR_ACCESS_TOKEN

4. Patient-Doctor Mapping APIs
Assign Doctor to Patient
httpPOST /api/mappings/
Content-Type: application/json
Authorization: Bearer YOUR_ACCESS_TOKEN

{
    "patient": 1,
    "doctor": 1,
    "is_active": true
}

Get All Mappings
httpGET /api/mappings/
Authorization: Bearer YOUR_ACCESS_TOKEN

Get Doctors for Specific Patient
httpGET /api/mappings/patients/1/
Authorization: Bearer YOUR_ACCESS_TOKEN

Remove Doctor from Patient
httpDELETE /api/mappings/1/
Authorization: Bearer YOUR_ACCESS_TOKEN

🧪 Testing Workflow
Step-by-step Testing:

Register a new user using the registration endpoint
Login with the registered user to get JWT tokens
Create a patient using the patient creation endpoint
Create a doctor using the doctor creation endpoint
Assign the doctor to the patient using the mapping endpoint
Test all GET endpoints to retrieve data
Test UPDATE endpoints to modify existing records
Test DELETE endpoints to remove records

Sample Test Data
Sample Patient Data:
json{
    "name": "Alice Johnson",
    "email": "alice.johnson@email.com",
    "phone": "+1555123456",
    "age": 28,
    "gender": "F",
    "address": "789 Oak Ave, Springfield, IL 62701"
}
Sample Doctor Data:
json{
    "name": "Dr. Sarah Wilson",
    "email": "sarah.wilson@medcenter.com",
    "phone": "+1555789012",
    "specialization": "PEDIATRICS",
    "license_number": "MD98765",
    "years_of_experience": 12,
    "hospital_affiliation": "Children's Medical Center",
    "consultation_fee": "120.00"
}

Environment Variables: Make sure to update the .env file with your actual database credentials
Secret Key: Change the SECRET_KEY in production
Pagination: API responses are paginated (20 items per page)
Permissions: Patient data is user-specific, but doctor data is shared across all users
