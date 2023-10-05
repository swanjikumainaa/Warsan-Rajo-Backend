from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .permissions import IsAdminOrNGO, IsHealthworker, IsOwnerOrAdmin, IsAdminOrReadOnly
from rest_framework.permissions import IsAuthenticated
from .serializers import (
    LocationSerializer,
    Immunization_RecordSerializer,
    CustomUserSerializer,
    HealthworkerSerializer,
    VaccineSerializer,
    ChildSerializer,
    GuardianSerializer,
    
)
from django.http import Http404
from location.models import Location
from Immunization_Record.models import Immunization_Record
from registration.models import CustomUser, Healthworker
from vaccine.models import Vaccine
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.hashers import make_password
from child.models import Child, Guardian
from django.contrib.auth import authenticate, login, logout

@api_view(['GET', 'POST'])
@permission_classes([IsAdminOrNGO])
def location_list(request):
    if request.method == 'GET':
        locations = Location.objects.all()
        serializer = LocationSerializer(locations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = LocationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAdminOrNGO])
def location_detail(request, id):
    try:
        location = Location.objects.get(id=id)
    except Location.DoesNotExist:
        return Response({'message': 'Location not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = LocationSerializer(location)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        serializer = LocationSerializer(location, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        location.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
@permission_classes([IsAdminOrNGO])
def immunization_record_list(request):
    if request.method == 'GET':
        immunization_records = Immunization_Record.objects.all()
        serializer = Immunization_RecordSerializer(immunization_records, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = Immunization_RecordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAdminOrNGO])
def immunization_record_detail(request, pk):
    try:
        immunization_record = Immunization_Record.objects.get(pk=pk)
    except Immunization_Record.DoesNotExist:
        return Response({'message': 'Immunization Record not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = Immunization_RecordSerializer(immunization_record)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        serializer = Immunization_RecordSerializer(immunization_record, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        immunization_record.delete()
        return Response("Immunization Record deleted", status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([IsAdminOrNGO])
def healthworker_signup(request):
    serializer = HealthworkerSerializer(data=request.data)
    if serializer.is_valid():
        password = request.data.get('password')
        hashed_password = make_password(password)
        healthworker = serializer.save(password=hashed_password)
        creator_id = request.data.get('created_by')
        if creator_id:
            creator = CustomUser.objects.filter(id=creator_id).first()
            if creator:
                healthworker.created_by = creator
                healthworker.save()
        return Response({'message': 'Health worker registered successfully'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAdminOrNGO])
def healthworker_logout(request):
    logout(request)
    return Response({'message': 'Health worker logged out successfully'}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsHealthworker])
def healthworker_login(request):
    phone_number = request.data.get('phone_number')
    password = request.data.get('password')
    user = Healthworker.objects.filter(phone_number=phone_number).first()
    if user is not None and user.check_password(password):
        login(request, user)
        token = default_token_generator.make_token(user)
        return Response({'token': token}, status=status.HTTP_200_OK)
    elif user is None:
        return Response({'message': 'User with this phone number does not exist'}, status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response({'message': 'Invalid password'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@permission_classes([IsAdminOrNGO])
def ngo_login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = CustomUser.objects.filter(username=username).first()
    if user is not None and user.check_password(password):
        login(request, user)
        token = default_token_generator.make_token(user)
        return Response({'token': token}, status=status.HTTP_200_OK)
    return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)



@api_view(['GET', 'POST'])
@permission_classes([IsAdminOrReadOnly])
def vaccine_list(request):
    if request.method == 'GET':
        vaccines = Vaccine.objects.all()
        serializer = VaccineSerializer(vaccines, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = VaccineSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAdminOrReadOnly])
def vaccine_detail(request, id):
    try:
        vaccine = Vaccine.objects.get(id=id)
    except Vaccine.DoesNotExist:
        return Response({'message': 'Vaccine not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = VaccineSerializer(vaccine)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        serializer = VaccineSerializer(vaccine, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        vaccine.delete()
        return Response("Vaccine Deleted", status=status.HTTP_204_NO_CONTENT)


# Views for CustomUser model
@api_view(['GET', 'POST'])
@permission_classes([IsAdminOrReadOnly])
def custom_user_list(request):
    if request.method == 'GET':
        custom_users = CustomUser.objects.all()
        serializer = CustomUserSerializer(custom_users, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(request.data.get('password'))
            user.save()
            return Response({'message': 'Custom user created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAdminOrReadOnly])
def custom_user_detail(request, pk):
    try:
        custom_user = CustomUser.objects.get(pk=pk)
    except CustomUser.DoesNotExist:
        return Response({'message': 'Custom user not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CustomUserSerializer(custom_user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        serializer = CustomUserSerializer(custom_user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        custom_user.delete()
        return Response("Custom user deleted", status=status.HTTP_204_NO_CONTENT)

# Views for Healthworker model
@api_view(['GET', 'POST'])
@permission_classes([IsAdminOrReadOnly])
def healthworker_list(request):
    if request.method == 'GET':
        healthworkers = Healthworker.objects.all()
        serializer = HealthworkerSerializer(healthworkers, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = HealthworkerSerializer(data=request.data)
        if serializer.is_valid():
            password = request.data.get('password')
            hashed_password = make_password(password)
            healthworker = serializer.save(password=hashed_password)
            creator_id = request.data.get('created_by')
            if creator_id:
                creator = CustomUser.objects.filter(id=creator_id).first()
                if creator:
                    healthworker.created_by = creator
                    healthworker.save()
            return Response({'message': 'Health worker registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsOwnerOrAdmin])
def healthworker_detail(request, pk):
    try:
        healthworker = Healthworker.objects.get(pk=pk)
    except Healthworker.DoesNotExist:
        return Response({'message': 'Health worker not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = HealthworkerSerializer(healthworker)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        serializer = HealthworkerSerializer(healthworker, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        healthworker.delete()
        return Response("Health worker deleted", status=status.HTTP_204_NO_CONTENT)


# Views for Vaccine model
@api_view(['GET', 'POST'])
@permission_classes([IsAdminOrReadOnly])
def vaccine_list(request):
    if request.method == 'GET':
        vaccines = Vaccine.objects.all()
        serializer = VaccineSerializer(vaccines, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = VaccineSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAdminOrReadOnly])
def vaccine_detail(request, id):
    try:
        vaccine = Vaccine.objects.get(id=id)
    except Vaccine.DoesNotExist:
        return Response({'message': 'Vaccine not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = VaccineSerializer(vaccine)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        serializer = VaccineSerializer(vaccine, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        vaccine.delete()
        return Response("Vaccine Deleted", status=status.HTTP_204_NO_CONTENT)

# Views for State, Region, and District
@api_view(['GET'])
@permission_classes([IsAdminOrReadOnly])
def state_list(request):
    states = Location.objects.values_list('state', flat=True).distinct()
    return Response(states, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAdminOrReadOnly])
def specific_region_list(request, state_name):
    regions = Location.objects.filter(state=state_name).values_list('region', flat=True).distinct()
    return Response(regions, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAdminOrReadOnly])
def specific_district_list(request, state_name, region_name):
    districts = Location.objects.filter(state=state_name, region=region_name).values_list('district', flat=True).distinct()
    return Response(districts, status=status.HTTP_200_OK)

# Views for Child and Guardian models
@api_view(['GET', 'POST'])
@permission_classes([IsAdminOrReadOnly])
def child_list(request):
    if request.method == 'GET':
        children = Child.objects.all()
        serializer = ChildSerializer(children, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ChildSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAdminOrReadOnly])
def child_detail(request, pk):
    try:
        child = Child.objects.get(pk=pk)
    except Child.DoesNotExist:
        return Response({'message': 'Child not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ChildSerializer(child)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        serializer = ChildSerializer(child, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        child.delete()
        return Response("Child deleted", status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
@permission_classes([IsAdminOrReadOnly])
def guardian_list(request):
    if request.method == 'GET':
        guardians = Guardian.objects.all()
        serializer = GuardianSerializer(guardians, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = GuardianSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAdminOrReadOnly])
def guardian_detail(request, pk):
    try:
        guardian = Guardian.objects.get(pk=pk)
    except Guardian.DoesNotExist:
        return Response({'message': 'Guardian not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = GuardianSerializer(guardian)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        serializer = GuardianSerializer(guardian, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        guardian.delete()
        return Response("Guardian deleted", status=status.HTTP_204_NO_CONTENT)

# Continue to define and implement other views as needed.
@api_view(['POST'])
@permission_classes([IsAdminOrNGO])
def ngo_signup(request):
    serializer = CustomUserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        user.set_password(request.data.get('password'))
        user.save()
        return Response({'message': 'NGO user created successfully'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAdminOrNGO])
def ngo_logout(request):
    logout(request)
    return Response({'message': 'NGO user logged out successfully'}, status=status.HTTP_200_OK)

# Views for Child and Guardian models
@api_view(['GET', 'POST'])
@permission_classes([IsAdminOrReadOnly])
def child_list(request):
    if request.method == 'GET':
        children = Child.objects.all()
        serializer = ChildSerializer(children, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ChildSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAdminOrReadOnly])
def child_detail(request, pk):
    try:
        child = Child.objects.get(pk=pk)
    except Child.DoesNotExist:
        return Response({'message': 'Child not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ChildSerializer(child)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        serializer = ChildSerializer(child, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        child.delete()
        return Response("Child deleted", status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
@permission_classes([IsAdminOrReadOnly])
def guardian_list(request):
    if request.method == 'GET':
        guardians = Guardian.objects.all()
        serializer = GuardianSerializer(guardians, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = GuardianSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAdminOrReadOnly])
def guardian_detail(request, pk):
    try:
        guardian = Guardian.objects.get(pk=pk)
    except Guardian.DoesNotExist:
        return Response({'message': 'Guardian not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = GuardianSerializer(guardian)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        serializer = GuardianSerializer(guardian, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        guardian.delete()
        return Response("Guardian deleted", status=status.HTTP_204_NO_CONTENT)
