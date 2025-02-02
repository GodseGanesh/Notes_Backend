from django.shortcuts import render
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from .models import Notes
from .serializers import NoteSerializer
from django.contrib.auth import authenticate,login as auth_login
from .serializers import *
from rest_framework import status
from rest_framework.permissions import IsAuthenticated,AllowAny



@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    print("Request data:", request.data)  # Debugging step
    
    
    serializer = UserRegistrationSerializer(data=request.data)
    
    if serializer.is_valid():
        user = serializer.save()
        print("User created:", user)  # Debugging step
        return Response({"message": "User registered successfully!"}, status=status.HTTP_201_CREATED)
    
    print("Validation errors:", serializer.errors)  # Debugging step
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    try:
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({"message": "Username and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)

        if user is not None:
            auth_login(request, user)
            return Response({
                "message": "User logged in successfully!",
                "username": user.username,
                "email": user.email  # Only serializable fields
            }, status=status.HTTP_200_OK)

        return Response({"message": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({"message": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def notes(request):

    if request.method == 'GET':
        obj=Notes.objects.filter(user=request.user).order_by('-updated')
        serializers=NoteSerializer(obj,many=True)
        return Response(serializers.data)
    
    if request.method == 'POST':
        data = request.data
        
        obj= Notes.objects.create(
            body=data['body'],
            user = request.user
        )
        serializer = NoteSerializer(obj,many=False)

        return Response(serializer.data)
    
    

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def note(request, pk):
    try:
        note = Notes.objects.get(id=pk, user=request.user)  # Ensure the note belongs to the current user
    except Notes.DoesNotExist:
        return Response({"error": "Note not found or not owned by the current user"}, status=404)

    if request.method == 'GET':
        serializer = NoteSerializer(note)
        return Response(serializer.data)

    if request.method == 'PUT':
        data = request.data
        serializer = NoteSerializer(instance=note, data=data)

        if serializer.is_valid():
            serializer.save()  # The user is already associated through the view
            return Response(serializer.data)

        return Response(serializer.errors, status=400)

    if request.method == 'DELETE':
        note.delete()
        return Response({"message": "Note was deleted"}, status=204)
