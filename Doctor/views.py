
# Create your views here.
from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Doctor,Otp
from .serializer import DoctorSerializer
import bcrypt
import jwt 
import datetime
from django.conf import settings
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
# from sendgrid.helpers.mail import Mail, Email, To, Content
# import sendgrid
import random

def get_token_from_request(request):
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return None
    try:
        token = auth_header.split(" ")[1]
        return jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    except (IndexError, jwt.DecodeError):
        return None
    


def decode_token(token):
    # Replace 'your_secret_key' with your actual secret key
    return jwt.decode(token, 'your_secret_key', algorithms=['HS256'])


@api_view(["POST"])
def create_doctor(request):
    data = request.data
    data["password"] = bcrypt.hashpw(
        data["password"].encode("utf-8"), bcrypt.gensalt()
    ).decode("utf-8")
    serializer = DoctorSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(["GET"])
def get_all_doctors(request):
    doctor = Doctor.objects.all()
    serializer = DoctorSerializer(doctor, many=True)
    return Response(serializer.data)



# @api_view(["GET"])
# def get_doctor_by_id(request):
#     token = get_token_from_request(request)
#     if not token:
#         return Response(
#             {"detail": "Authentication credentials were not provided."},
#             status=status.HTTP_401_UNAUTHORIZED,
#         )
#     try:
#         decoded_token = decode_token(token)  
#         doctor_id = decoded_token.get("doctor_id") 
#     except Exception as e:
#         return Response(
#             {"detail": "Invalid or expired token."},
#             status=status.HTTP_401_UNAUTHORIZED,
#         )
#     doctor = get_object_or_404(Doctor, id=doctor_id)
#     if not doctor.is_verify:
#         return Response(
#             {"message": "Patient not verified"}, status=status.HTTP_403_FORBIDDEN
#         )
#     serializer = DoctorSerializer(doctor)
#     return Response(serializer.data)


@api_view(["GET"])
def get_doctor_by_id(request):
    decoded_token = get_token_from_request(request)
    if not decoded_token:
        return Response(
            {"detail": "Authentication credentials were not provided."},
            status=status.HTTP_401_UNAUTHORIZED,
        )
    print(decoded_token)
    doctor_id = decoded_token["doctor_id"]
    doctor = get_object_or_404(Doctor, id=doctor_id)
    if not doctor.is_verify:
        return Response(
            {"message": "User not verified"}, status=status.HTTP_403_FORBIDDEN
        )
    serializer = DoctorSerializer(doctor)
    return Response(serializer.data)



@api_view(["PUT"])
def update_doctor(request):
    token = get_token_from_request(request)
    if not token:
        return Response(
            {"detail": "Authentication credentials were not provided."},
            status=status.HTTP_401_UNAUTHORIZED,
        )
    decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
    doctor_id = decoded_token.get("doctor_id")  
    
    doctor = get_object_or_404(Doctor, id=doctor_id)
    if not doctor.is_verify:
        return Response(
            {"message": "Doctor not verified"}, status=status.HTTP_403_FORBIDDEN
        )
    if doctor.is_deleted:
        return Response(
            {"message": "Doctor is deleted"}, status=status.HTTP_403_FORBIDDEN
        )
    if not doctor.is_active:
        return Response(
            {"message": "Doctor is not active"}, status=status.HTTP_403_FORBIDDEN
        )
    
@api_view(["PUT"])
def update_doctor(request):
    token = get_token_from_request(request)
    if not token:
        return Response(
            {"detail": "Authentication credentials were not provided."},
            status=status.HTTP_401_UNAUTHORIZED,
        )
    decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
    doctor_id = decoded_token.get("doctor_id")  
    
    doctor = get_object_or_404(Doctor, id=doctor_id)
    if not doctor.is_verify:
        return Response(
            {"message": "Patient not verified"}, status=status.HTTP_403_FORBIDDEN
        )
    if doctor.is_deleted:
        return Response(
            {"message": "Patient is deleted"}, status=status.HTTP_403_FORBIDDEN
        )
    if not doctor.is_active:
        return Response(
            {"message": "Patient is not active"}, status=status.HTTP_403_FORBIDDEN
        )
    # Update patient data
    data = request.data
    if "password" in data:
        data["password"] = bcrypt.hashpw(
            data["password"].encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")
    
    serializer = DoctorSerializer(doctor, data=data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(["DELETE"])
def delete_doctor(request):
    token = get_token_from_request(request)
    if not token:
        return Response(
            {"detail": "Authentication credentials were not provided."},
            status=status.HTTP_401_UNAUTHORIZED,
        )
    decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
    doctor_id = decoded_token.get("patient_id") 
    doctor = get_object_or_404(Doctor, id=doctor_id)
    
    if doctor.is_deleted:
        return Response(
            {"message": "Patient already deleted"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    if not doctor.is_verify:
        return Response(
            {"message": "Patient not verified"}, status=status.HTTP_403_FORBIDDEN
        )
    doctor.is_deleted = True
    doctor.is_active = False
    doctor.save()

    return Response(
        {"message": "Patient deleted successfully"}, status=status.HTTP_204_NO_CONTENT
    )



@api_view(["POST"])
def generate_otp(request):
    email = request.data.get("email")
    patient = get_object_or_404(Doctor, email=email)
    otp = str(random.randint(100000, 999999))
    Otp.objects.create(patient=patient, email=email, otp=otp)

    # Send OTP email
    # msg = MIMEMultipart()
    # msg["From"] = settings.EMAIL_HOST_USER
    # msg["To"] = email
    # msg["Subject"] = "Your OTP Code"
    # msg.attach(MIMEText(f"Your OTP code is {otp}", "plain"))
    # server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
    # server.starttls()
    # server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
    # server.sendmail(settings.EMAIL_HOST_USER, email, msg.as_string())
    # server.quit()

    return Response({"message": "OTP sent successfully"}, status=status.HTTP_200_OK)


    

@api_view(["POST"])
def verify_otp(request):
    email = request.data.get("email")
    otp = request.data.get("otp")
    otp_record = get_object_or_404(Otp, email=email, otp=otp)
    if otp_record:
        patient = otp_record.patient
        patient.is_verify = True
        patient.save()
        otp_record.delete()  # Delete the OTP record after successful verification
        return Response(
            {"message": "OTP verified successfully"}, status=status.HTTP_200_OK
        )
    return Response({"message": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)



@api_view(["POST"])
def login(request):
    email = request.data.get("email")
    password = request.data.get("password")
    if not email or not password:
        return Response({"error": "Email and password are required"}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        doctor = Doctor.objects.get(email=email)
    except Doctor.DoesNotExist:
        return Response({"error": "Doctor not found"}, status=status.HTTP_404_NOT_FOUND)

    if not bcrypt.checkpw(password.encode("utf-8"), doctor.password.encode("utf-8")):
        return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
    
    if not doctor.is_verify:
        return Response({"error": "Doctor not verified"}, status=status.HTTP_403_FORBIDDEN)
    
    payload = {
        "patient_id": str(doctor.id),
        "email": doctor.email,
        "exp": datetime.datetime.now() + datetime.timedelta(hours=24),
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
    return Response({"token": token}, status=status.HTTP_200_OK)



@api_view(["POST"])
def forgot_password(request):
    email = request.data.get("email")
    new_password = request.data.get("new_password")
    if not email or not new_password:
        return Response({"error": "Email and new password are required"}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        doctor = Doctor.objects.get(email=email)
        doctor.password = bcrypt.hashpw(new_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        doctor.save()
        return Response({"message": "Password updated successfully"}, status=status.HTTP_200_OK)
    except Doctor.DoesNotExist:
        return Response({"error": "Patient not found"}, status=status.HTTP_404_NOT_FOUND)

