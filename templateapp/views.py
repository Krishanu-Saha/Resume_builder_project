from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import ResumeTemplate
from .serializers import ResumeTemplateSerializer

@api_view(['GET'])
def template_list(request):
    templates = ResumeTemplate.objects.all()
    # ✅ Pass request into serializer context so use_url=True returns absolute URLs
    serializer = ResumeTemplateSerializer(templates, many=True, context={'request': request})
    return Response(serializer.data)


# Create your views here.
