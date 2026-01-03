from django.shortcuts import render
from .models import Note
from .serializers import NoteSerializer, RegisterSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import  status
from rest_framework.permissions import IsAuthenticated, AllowAny



# Create your views here.

@api_view(["GET","POST"])
@permission_classes([IsAuthenticated])
def notes(request):
    if request.method == "GET":
        notes = Note.objects.filter(user=request.user).order_by('-created')
        serializer = NoteSerializer(notes, many=True)
        return Response(serializer.data)
    
    elif request.method == "POST":
        serializer = NoteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET","PUT","DELETE"])
@permission_classes([IsAuthenticated])
def note_detail(request,slug):
    try:
        note = Note.objects.get(slug=slug, user=request.user)
    except Note.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == "GET":
        serializer = NoteSerializer(note)
        return Response(serializer.data)
    elif request.method == "PUT":
        serializer = NoteSerializer(note,data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status = status.HTTP_200_OK)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
    
    elif request.method == "DELETE":
        note.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)



@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "User registered successfully"},status= status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


