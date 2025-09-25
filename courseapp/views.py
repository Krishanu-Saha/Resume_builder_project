# courseapp/views.py
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import Course
from .serializers import CourseSerializer
from accountapp.authentication import JWTAuthentication
from accountapp.permissions import IsResumeOwnerOrAdmin
from rest_framework.permissions import IsAuthenticated


@api_view(['GET', 'POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def course_list_create(request, resume_id):
    """
    List all courses for a resume (owned by the user) or create a new course.
    """
    from resume.models import Resume
    resume = get_object_or_404(Resume, id=resume_id)

    # enforce ownership
    if resume.user != request.user:
        return Response({'detail': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        courses = resume.courses.all()
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = CourseSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(resume=resume)  # enforce resume assignment
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, IsResumeOwnerOrAdmin])
def course_detail(request, resume_id, pk):
    course = get_object_or_404(Course, pk=pk, resume_id=resume_id)

    # Ownership check
    if course.resume.user != request.user:
        return Response({"detail": "Not authorized"}, status=403)

    if request.method == 'GET':
        serializer = CourseSerializer(course)
        return Response(serializer.data)

    if request.method in ['PUT', 'PATCH']:
        serializer = CourseSerializer(
            course,
            data=request.data,
            partial=(request.method == 'PATCH'),
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save(resume=course.resume)  # prevent changing resume
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        course.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
