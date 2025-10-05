# profileapp/views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Profile
from .serializers import ProfileSerializer
from accountapp.permissions import IsResumeOwnerOrAdmin
from accountapp.authentication import JWTAuthentication


class ProfileMeView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsResumeOwnerOrAdmin]  # ✅ uses JWTAuthentication globally

    # CREATE profile
    def post(self, request):
        if hasattr(request.user, "profile"):
            return Response(
                {"detail": "Profile already exists. Use PUT to update."},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = ProfileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # READ profile
    def get(self, request):
        try:
            profile = request.user.profile
            serializer = ProfileSerializer(profile)
            return Response(serializer.data)
        except Profile.DoesNotExist:
            return Response(
                {"detail": "Profile does not exist. Use POST to create."},
                status=status.HTTP_404_NOT_FOUND
            )

    # UPDATE profile
    def put(self, request):
        try:
            profile = request.user.profile
        except Profile.DoesNotExist:
            return Response(
                {"detail": "Profile does not exist. Use POST to create."},
                status=status.HTTP_404_NOT_FOUND
            )

        self.check_object_permissions(request, profile)
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    # DELETE profile
    def delete(self, request):
        try:
            profile = request.user.profile
            self.check_object_permissions(request, profile)
            profile.delete()
            return Response({"detail": "Profile deleted successfully."})
        except Profile.DoesNotExist:
            return Response(
                {"detail": "Profile does not exist."},
                status=status.HTTP_404_NOT_FOUND
            )
