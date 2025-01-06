from django.shortcuts import render
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from .models import Notes
from .serializers import NoteSerializer
from django.contrib.auth import authenticate,login
from .serializers import *
from rest_framework import status
from rest_framework.permissions import IsAuthenticated,AllowAny



@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    print(request.data)
    serializer = UserRegistrationSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "User registered successfully!"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(username=username,password=password)
    if user is not None:
        login(request, user)
        return Response({"message": "User registered successfully!","user":request.user}, status=status.HTTP_200_OK)
    return Response({"message": "Invalid Creadientials"}, status=status.HTTP_400_BAD_REQUEST)


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
    
    

@api_view(['GET','PUT','DELETE'])
@permission_classes([IsAuthenticated])
def note(request,pk):

    if request.method == 'GET':
        obj= Notes.objects.get(id=pk)
        serializers = NoteSerializer(obj,many=False)
        return Response(serializers.data)
    
    if request.method == 'PUT':
        data = request.data
        
        obj= Notes.objects.get(id=pk)
        serializer = NoteSerializer(instance=obj,data=data,user = request.user)

        if serializer.is_valid():
            serializer.save()

        return Response(serializer.data)
    
    if request.method == 'DELETE':
        obj= Notes.objects.get(id=pk)
        obj.delete()
        return Response("Note was deleted")
    
    if request.method == 'PUT':
        obj = Notes.objects.get(id=pk)
        

