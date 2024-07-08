from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Notes
from .serializers import NoteSerializer


@api_view(['GET','POST'])
def notes(request):

    if request.method == 'GET':
        obj=Notes.objects.all().order_by('-updated')
        serializers=NoteSerializer(obj,many=True)
        return Response(serializers.data)
    
    if request.method == 'POST':
        data = request.data
        obj= Notes.objects.create(
            body=data['body']
        )
        serializer = NoteSerializer(obj,many=False)

        return Response(serializer.data)
    
    

@api_view(['GET','PUT','DELETE'])
def note(request,pk):

    if request.method == 'GET':
        obj= Notes.objects.get(id=pk)
        serializers = NoteSerializer(obj,many=False)
        return Response(serializers.data)
    
    if request.method == 'PUT':
        data = request.data
        obj= Notes.objects.get(id=pk)
        serializer = NoteSerializer(instance=obj,data=data)

        if serializer.is_valid():
            serializer.save()

        return Response(serializer.data)
    
    if request.method == 'DELETE':
        obj= Notes.objects.get(id=pk)
        obj.delete()
        return Response("Note was deleted")

# @api_view(['PUT'])
# def update(request,pk):
#     data = request.data
#     obj= Notes.objects.get(id=pk)
#     serializer = NoteSerializer(instance=obj,data=data)

#     if serializer.is_valid():
#         serializer.save()

#     return Response(serializer.data)

# @api_view(['DELETE'])
# def delete(request,pk):
#     obj= Notes.objects.get(id=pk)
#     obj.delete()
#     return Response("Note was deleted")


# @api_view(['POST'])
# def create(request):
#     data = request.data
#     obj= Notes.objects.create(
#         body=data['body']
#     )
#     serializer = NoteSerializer(obj,many=False)

#     return Response(serializer.data)
