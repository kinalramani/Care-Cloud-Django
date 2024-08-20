from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Patient,Otp
from .serializer import PatientSerializer
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



#----------------------------------------------------------get_token_from_request----------------------------


def get_token_from_request(request):
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return None
    try:
        token = auth_header.split(" ")[1]
        return jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    except (IndexError, jwt.DecodeError):
        return None
    


#----------------------------------------------create patient---------------------------------------------

@api_view(["POST"])
def create_patient(request):
    data = request.data
    data["password"] = bcrypt.hashpw(
        data["password"].encode("utf-8"), bcrypt.gensalt()
    ).decode("utf-8")
    serializer = PatientSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#-----------------------------------------------------get all patient--------------------------------------


@api_view(["GET"])
def get_all_patients(request):
    patient = Patient.objects.all()
    serializer = PatientSerializer(patient, many=True)
    return Response(serializer.data)


#------------------------------------------------------get patient by id------------------------------------------

# @api_view(["GET"])
# def get_patient_by_id(request):
#     # breakpoint()
#     token = get_token_from_request(request)
#     if not token:
#         return Response(
#             {"detail": "Authentication credentials were not provided."},
#             status=status.HTTP_401_UNAUTHORIZED,
#         ) 
#     try:
#         decoded_token = decode_token(token)  
#         patient_id = decoded_token.get("patient_id") 
#     except Exception as e:
#         return Response(
#             {"detail": "Invalid or expired token."},
#             status=status.HTTP_401_UNAUTHORIZED,
#         )
#     patient = get_object_or_404(Patient, id=patient_id)
#     if not patient.is_verify:
#         return Response(
#             {"message": "Patient not verified"}, status=status.HTTP_403_FORBIDDEN
#         )
#     serializer = PatientSerializer(patient)
#     return Response(serializer.data)




def decode_token(token):
    try:
        decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        return decoded
    except jwt.ExpiredSignatureError:
        raise Exception("Token has expired")
    except jwt.InvalidTokenError:
        raise Exception("Invalid token")

@api_view(["GET"])
def get_patient_by_id(request):
    token = get_token_from_request(request)
    if not token:
        print("No token provided.")
        return Response(
            {"detail": "Authentication credentials were not provided."},
            status=status.HTTP_401_UNAUTHORIZED,
        )
    try:
        decoded_token = decode_token(token)
        print(f"Decoded Token: {decoded_token}")
        patient_id = decoded_token.get("patient_id")
        if not patient_id:
            print("No patient_id in token.")
            return Response(
                {"detail": "Token is invalid."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
    except Exception as e:
        print(f"Error decoding token: {e}")
        return Response(
            {"detail": str(e)},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    patient = get_object_or_404(Patient, id=patient_id)
    print(f"Patient Found: {patient}")

    # Skip verification check
    serializer = PatientSerializer(patient)
    return Response(serializer.data)


#------------------------------------------------------------------update patient-----------------------------

@api_view(["PUT"])
def update_patient(request):
    token = get_token_from_request(request)
    if not token:
        return Response(
            {"detail": "Authentication credentials were not provided."},
            status=status.HTTP_401_UNAUTHORIZED,
        )
    decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
    patient_id = decoded_token.get("patient_id")  
    
    patient = get_object_or_404(Patient, id=patient_id)
    if not patient.is_verify:
        return Response(
            {"message": "Patient not verified"}, status=status.HTTP_403_FORBIDDEN
        )
    if patient.is_deleted:
        return Response(
            {"message": "Patient is deleted"}, status=status.HTTP_403_FORBIDDEN
        )
    if not patient.is_active:
        return Response(
            {"message": "Patient is not active"}, status=status.HTTP_403_FORBIDDEN
        )
    
# @api_view(["PUT"])
# def update_patient(request):
#     token = get_token_from_request(request)
#     if not token:
#         return Response(
#             {"detail": "Authentication credentials were not provided."},
#             status=status.HTTP_401_UNAUTHORIZED,
#         )
#     decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
#     patient_id = decoded_token.get("patient_id")  
    
#     patient = get_object_or_404(Patient, id=patient_id)
#     if not patient.is_verify:
#         return Response(
#             {"message": "Patient not verified"}, status=status.HTTP_403_FORBIDDEN
#         )
#     if patient.is_deleted:
#         return Response(
#             {"message": "Patient is deleted"}, status=status.HTTP_403_FORBIDDEN
#         )
#     if not patient.is_active:
#         return Response(
#             {"message": "Patient is not active"}, status=status.HTTP_403_FORBIDDEN
#         )
#     # Update patient data
#     data = request.data
#     if "password" in data:
#         data["password"] = bcrypt.hashpw(
#             data["password"].encode("utf-8"), bcrypt.gensalt()
#         ).decode("utf-8")
    
#     serializer = PatientSerializer(patient, data=data, partial=True)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data)
    
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#------------------------------------------------------delete patient-----------------------------------------


    
@api_view(["DELETE"])
def delete_patient(request):
    token = get_token_from_request(request)
    if not token:
        return Response(
            {"detail": "Authentication credentials were not provided."},
            status=status.HTTP_401_UNAUTHORIZED,
        )
    decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
    patient_id = decoded_token.get("patient_id") 
    patient = get_object_or_404(Patient, id=patient_id)
    
    if patient.is_deleted:
        return Response(
            {"message": "Patient already deleted"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    if not patient.is_verify:
        return Response(
            {"message": "Patient not verified"}, status=status.HTTP_403_FORBIDDEN
        )
    patient.is_deleted = True
    patient.is_active = False
    patient.save()

    return Response(
        {"message": "Patient deleted successfully"}, status=status.HTTP_204_NO_CONTENT
    )


#-----------------------------------------------------generate otp ----------------------------------

@api_view(["POST"])
def generate_otp(request):
    email = request.data.get("email")
    patient = get_object_or_404(Patient, email=email)
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



#------------------------------------------------verify otp-------------------------------------------


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



#--------------------------------------------------------logging-----------------------------------

# @api_view(["POST"])
# def login(request):
#     email = request.data.get("email")
#     password = request.data.get("password")
#     if not email or not password:
#         return Response({"error": "Email and password are required"}, status=status.HTTP_400_BAD_REQUEST)
    
#     try:
#         patient = Patient.objects.get(email=email)
#     except Patient.DoesNotExist:
#         return Response({"error": "Patient not found"}, status=status.HTTP_404_NOT_FOUND)

#     if not bcrypt.checkpw(password.encode("utf-8"), patient.password.encode("utf-8")):
#         return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
    
#     if not patient.is_verify:
#         return Response({"error": "Patient not verified"}, status=status.HTTP_403_FORBIDDEN)
    
#     payload = {
#         "patient_id": str(patient.id),
#         "email": patient.email,
#         "exp": datetime.datetime.now() + datetime.timedelta(hours=24),
#     }
#     token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
#     return Response({"token": token}, status=status.HTTP_200_OK)


@api_view(["POST"])
def login(request):
    email = request.data.get("email")
    password = request.data.get("password")

    try:
        patient = Patient.objects.get(email=email)
    except Patient.DoesNotExist:
        try:
            patient = Patient.objects.get(email=email)
        except Patient.DoesNotExist:
            return Response(
                {"message": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST
            )

    # Verify the password
    if bcrypt.checkpw(password.encode("utf-8"), patient.password.encode("utf-8")):
        if not patient.is_verify:
            return Response(
                {"message": "User not verified"}, status=status.HTTP_403_FORBIDDEN
            )

        # Generate JWT token
        payload = {
            "patient_id": str(patient.id),
            "patient_name": patient.f_name,
            "exp": datetime.datetime.now()
            + datetime.timedelta(hours=1),  # Token expires in 1 hour
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

        return Response({"token": token}, status=status.HTTP_200_OK)
    else:
        return Response(
            {"message": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST
        )


#------------------------------------------------- forget password----------------------------------------

@api_view(["POST"])
def forgot_password(request):
    email = request.data.get("email")
    new_password = request.data.get("new_password")
    if not email or not new_password:
        return Response({"error": "Email and new password are required"}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        patient = Patient.objects.get(email=email)
        patient.password = bcrypt.hashpw(new_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        patient.save()
        return Response({"message": "Password updated successfully"}, status=status.HTTP_200_OK)
    except Patient.DoesNotExist:
        return Response({"error": "Patient not found"}, status=status.HTTP_404_NOT_FOUND)



#---------------------------------------------decode token -------------------------------------------------  


@api_view(["POST"])
def decode_token_view(request):
    token = get_token_from_request(request)
    if not token:
        return Response(
            {"detail": "Authentication credentials were not provided."},
            status=status.HTTP_401_UNAUTHORIZED,
        )
    try:
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        return Response(decoded_token, status=status.HTTP_200_OK)
    except jwt.ExpiredSignatureError:
        return Response(
            {"detail": "Token has expired."},
            status=status.HTTP_401_UNAUTHORIZED,
        )
    except jwt.InvalidTokenError:
        return Response(
            {"detail": "Invalid token."},
            status=status.HTTP_401_UNAUTHORIZED,
        )
    except Exception as e:
        return Response(
            {"detail": f"Token decoding error: {str(e)}"},
            status=status.HTTP_401_UNAUTHORIZED,
        )
    


