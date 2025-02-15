from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..serializers.serializer_user import UserSerializer
from drf_spectacular.utils import extend_schema

class CreateUserView(APIView):
    """
    API for user registration.
    """

    @extend_schema(
        summary="Register a New User",
        description="Creates a new user account with the provided details.",
        request=UserSerializer,
        responses={
            201: UserSerializer,
            400: {"message": "Invalid input data"},
        }
    )
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
