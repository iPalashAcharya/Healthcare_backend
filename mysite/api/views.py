from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .models import Patient, Doctor, PatientDoctorMapping
from .serializers import (
    UserRegistrationSerializer, 
    UserLoginSerializer,
    PatientSerializer, 
    DoctorSerializer, 
    PatientDoctorMappingSerializer
)

# Authentication Views
@api_view(['POST']) #restricts the view to POST request only
@permission_classes([AllowAny]) #bypasses default drf permissions and allows unauthenticated users to access this
def register_user(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()  #new user is created and saved to the db
        refresh = RefreshToken.for_user(user)
        return Response({
            'message': 'User registered successfully',
            'user': {
                'id': user.id,
                'name': f"{user.first_name} {user.last_name}",
                'email': user.email,
            },
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():    #runs the serializer's validate method
        user = serializer.validated_data['user'] #validated_data contains the attr dict with the user instance 
        refresh = RefreshToken.for_user(user) #get the jwt tokens for the logged in user
        return Response({
            'message': 'Login successful',
            'user': {
                'id': user.id,
                'name': f"{user.first_name} {user.last_name}",
                'email': user.email,
            },
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Patient Views
class PatientListCreateView(generics.ListCreateAPIView): #generic views save boilerplate code, this one combines GET(all) and POST ie GET/patients/ and POST/patients/
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated] #only authenticated users can access the view

    def get_queryset(self):  #overriding drf's default queryset logic to return only the patients created by the logged in user
        return Patient.objects.filter(created_by=self.request.user)
#above view gives all the patients created by the logged in user on GET request and created a new patient with PatientSerializer.create() method on POST request

class PatientDetailView(generics.RetrieveUpdateDestroyAPIView): #Handles GET, PUT, PATCH, DELETE for single patient record
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Patient.objects.filter(created_by=self.request.user) #limits access to only those patients that were created by the currently logged in user

# Doctor Views
class DoctorListCreateView(generics.ListCreateAPIView):
    queryset = Doctor.objects.all() #not filtering the queryset because doctors should be accessible to every user and every user should be able to assign a doctor to their patient
    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAuthenticated]

class DoctorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Doctor.objects.all() 
    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAuthenticated]

# PatientDoctor Mapping Views, allows logged in users to list and create PatientDoctor assignments
class PatientDoctorMappingListCreateView(generics.ListCreateAPIView):
    serializer_class = PatientDoctorMappingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return PatientDoctorMapping.objects.filter(
            patient__created_by=self.request.user,
            is_active=True
        ) #get all active mappings where the patient belongs to the logged in user

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_patient_doctors(request, patient_id): #viewing doctors assigned to the patient, given patient id fetch all the active mappings to the assigned doc
    patient = get_object_or_404(Patient, id=patient_id, created_by=request.user) #fetch the patient only if created by the logged in user otherwise return 404
    mappings = PatientDoctorMapping.objects.filter(patient=patient, is_active=True) #get all mappings for this patient
    serializer = PatientDoctorMappingSerializer(mappings, many=True) #serializes list of mapping to json
    return Response(serializer.data)

@api_view(['DELETE']) #used for disabling a mapping between doc and patient accepts DELETE request
@permission_classes([permissions.IsAuthenticated])
def remove_patient_doctor_mapping(request, mapping_id):
    mapping = get_object_or_404(
        PatientDoctorMapping, 
        id=mapping_id, 
        patient__created_by=request.user
    ) #used to get the mapping with id and which was created by the logged in user
    mapping.is_active = False #soft delete the mapping but keep in db for reporting purposes
    mapping.save()
    return Response({'message': 'Doctor removed from patient successfully'}, status=status.HTTP_200_OK)