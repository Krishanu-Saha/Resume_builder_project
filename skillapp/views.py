from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Skill
from .serializers import SkillSerializer
from resume.models import Resume

@api_view(['GET', 'POST'])
def skill_list_create(request, resume_id):
    if request.method == 'GET':
        skills = Skill.objects.filter(resume_id=resume_id)
        serializer = SkillSerializer(skills, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = request.data.copy()
        data["resume"] = resume_id   # attach skill to resume automatically
        serializer = SkillSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def skill_detail(request, resume_id, pk):
    try:
        skill = Skill.objects.get(pk=pk, resume_id=resume_id)
    except Skill.DoesNotExist:
        return Response({"error": "Skill not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SkillSerializer(skill)
        return Response(serializer.data)

    elif request.method == 'PUT':
        data = request.data.copy()
        data["resume"] = resume_id   # ensure skill stays linked to the same resume
        serializer = SkillSerializer(skill, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        skill.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Create your views here.
