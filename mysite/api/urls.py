from django.urls import path
from . import views

urlpatterns = [
    # Authentication urls
    path('auth/register/', views.register_user, name='register'),
    path('auth/login/', views.login_user, name='login'),
    
    # Patient urls
    path('patients/', views.PatientListCreateView.as_view(), name='patient-list-create'),
    path('patients/<int:pk>/', views.PatientDetailView.as_view(), name='patient-detail'),
    
    # Doctor urls
    path('doctors/', views.DoctorListCreateView.as_view(), name='doctor-list-create'),
    path('doctors/<int:pk>/', views.DoctorDetailView.as_view(), name='doctor-detail'),
    
    # PatientDoctor Mapping urls
    path('mappings/', views.PatientDoctorMappingListCreateView.as_view(), name='mapping-list-create'),
    path('mappings/patient/<int:patient_id>/', views.get_patient_doctors, name='patient-doctors'),
    path('mappings/<int:mapping_id>/', views.remove_patient_doctor_mapping, name='remove-mapping'),
]