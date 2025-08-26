from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Resume
from django.http import HttpResponse
from .serializers import ResumeSerializer
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string

@api_view(['GET', 'POST'])
def resume_list_create(request):
    if request.method == 'GET':
        resumes = Resume.objects.all()
        serializer = ResumeSerializer(resumes, many=True,context={'request': request})
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer = ResumeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def resume_detail(request, pk):
    resume = get_object_or_404(Resume, pk=pk)

    if request.method == 'GET':
        serializer = ResumeSerializer(resume,context={'request': request})
        return Response(serializer.data)

    if request.method in ['PUT', 'PATCH']:
        serializer = ResumeSerializer(resume, data=request.data, partial=(request.method == 'PATCH'))
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        resume.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
    
def preview_resume(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id)
    template_file = resume.template.file.path  # get HTML template file
    
    html = render_to_string(template_file, {"resume": resume})
    return HttpResponse(html)
