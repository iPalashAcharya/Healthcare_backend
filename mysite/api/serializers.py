from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Patient, Doctor, PatientDoctorMapping

class UserRegistrationSerializer(serializers.ModelSerializer): #model serializers are used to map model fields automatically
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password', 'password_confirm')

    def validate_email(self, value):           #triggered automatically when using serializers.is_valid for every field drf looks for a method like validate_<fieldname> in the serializer when is_valid() is triggered
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def validate(self, attrs):  #after all fields are validated, drf checks whether validate is defined and its run
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match.")
        return attrs

    def create(self, validated_data): #if is_valid returns true and you serializer.save() then drf will run this create function
        validated_data.pop('password_confirm')
        user = User.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password']
        )
        return user

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(username=email, password=password) #returns a django user instance if true returns none if the credentials are invalid
            if not user:
                raise serializers.ValidationError('Invalid credentials.')
            if not user.is_active:
                raise serializers.ValidationError('User account is disabled.')
            attrs['user'] = user  #added the user to the attrs dict which contains email and password
        else:
            raise serializers.ValidationError('Must include email and password.')
        return attrs

class PatientSerializer(serializers.ModelSerializer):
    created_by_name = serializers.SerializerMethodField(read_only=True) #done to display created by user's name and not the user id from the User model, serializer method field looks for a method named exactly get_created_by_name

    class Meta:
        model = Patient
        fields = '__all__'
        read_only_fields = ('created_by', 'created_at', 'updated_at')

    def get_created_by_name(self, obj):
        return f"{obj.created_by.first_name} {obj.created_by.last_name}"

    def create(self, validated_data):  #create will be called when you serializer.save
        validated_data['created_by'] = self.context['request'].user #self.context is a dictionary that DRF automatically populates with the current request if you pass it when creating the serializer, so you have access to the current user.
        return super().create(validated_data) #new patient is created with the current logged in user as created by (Patient.objects.create(validated_data))

class DoctorSerializer(serializers.ModelSerializer):
    created_by_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Doctor
        fields = '__all__'
        read_only_fields = ('created_by', 'created_at', 'updated_at')

    def get_created_by_name(self, obj):
        return f"{obj.created_by.first_name} {obj.created_by.last_name}"

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)

class PatientDoctorMappingSerializer(serializers.ModelSerializer):
    patient_name = serializers.SerializerMethodField(read_only=True)
    doctor_name = serializers.SerializerMethodField(read_only=True)
    doctor_specialization = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = PatientDoctorMapping
        fields = '__all__'
        read_only_fields = ('created_by', 'assigned_date')

    def get_patient_name(self, obj):
        return obj.patient.name

    def get_doctor_name(self, obj):
        return obj.doctor.name

    def get_doctor_specialization(self, obj):
        return obj.doctor.speciality

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)

    def validate(self, attrs):
        patient = attrs.get('patient')
        doctor = attrs.get('doctor')
        
        # Check if the user has access to the patient
        if patient.created_by != self.context['request'].user:
            raise serializers.ValidationError("You can only assign doctors to your own patients.")
        
        return attrs