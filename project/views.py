from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import Project
from .serializers import ProjectSerializer
from resume.models import Resume


@api_view(["GET", "POST"])
def project_list_create(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id)

    if request.method == "GET":
        projects = Project.objects.filter(resume=resume)
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(resume=resume)  # ✅ set resume automatically
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
def project_detail(request, resume_id, pk):
    project = get_object_or_404(Project, pk=pk, resume_id=resume_id)

    if request.method == "GET":
        serializer = ProjectSerializer(project)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = ProjectSerializer(project, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(resume=project.resume)  # ✅ keep same resume
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Create your views here.
