from django.contrib import admin
from .models import Patient, Doctor, PatientDoctorMapping

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'age', 'gender', 'created_by', 'created_at')
    list_filter = ('gender', 'created_at', 'created_by')
    search_fields = ('name', 'email', 'phone')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'speciality', 'years_of_experience', 'created_by', 'created_at')
    list_filter = ('speciality', 'created_at', 'created_by')
    search_fields = ('name', 'email', 'license_number')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(PatientDoctorMapping)
class PatientDoctorMappingAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'assigned_date', 'is_active', 'created_by')
    list_filter = ('assigned_date', 'is_active', 'created_by')
    search_fields = ('patient__name', 'doctor__name')
