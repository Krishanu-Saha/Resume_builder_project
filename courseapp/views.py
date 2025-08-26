from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import Course
from .serializers import CourseSerializer
from resume.models import Resume


@api_view(['GET', 'POST'])
def course_list_create(request, resume_id):
    # Ensure the resume exists
    resume = get_object_or_404(Resume, id=resume_id)

    if request.method == 'GET':
        courses = Course.objects.filter(resume=resume)
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = request.data.copy()
        data["resume"] = resume.id   # link to given resume
        serializer = CourseSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def course_detail(request, resume_id, pk):
    # Ensure course belongs to the given resume
    course = get_object_or_404(Course, pk=pk, resume_id=resume_id)

    if request.method == 'GET':
        serializer = CourseSerializer(course)
        return Response(serializer.data)

    elif request.method == 'PUT':
        data = request.data.copy()
        data["resume"] = course.resume.id  # prevent resume change
        serializer = CourseSerializer(course, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        course.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
