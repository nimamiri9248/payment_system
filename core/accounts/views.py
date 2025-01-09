
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.tokens import TokenError
from .serializers import LogoutSerializer, RegisterSerializer, UserProfileSerializer


class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {
                    "message": "User registered successfully.",
                    "result": {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                    }
                },
                status=status.HTTP_201_CREATED
            )
        return Response(
            {
                "message": "Validation error",
                "result": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )


class UserProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get(self, request):
        """
        Retrieve the profile of the logged-in user.
        """
        serializer = self.serializer_class(request.user)
        return Response(
            {
                "message": "User profile retrieved successfully.",
                "result": serializer.data
            },
            status=status.HTTP_200_OK
        )

    def patch(self, request):
        serializer = self.serializer_class(
            request.user,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {
                    "message": "User profile updated (partial).",
                    "result": self.serializer_class(user).data
                },
                status=status.HTTP_200_OK
            )
        return Response(
            {
                "message": "Validation error",
                "result": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    def put(self, request):
        serializer = self.serializer_class(
            request.user, 
            data=request.data
        )
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {
                    "message": "User profile updated (full).",
                    "result": self.serializer_class(user).data
                },
                status=status.HTTP_200_OK
            )
        return Response(
            {
                "message": "Validation error",
                "result": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )
        
class LogoutView(APIView):
    """
    Handles user logout by blacklisting the refresh token.
    The client must send the 'refresh' token in the request body.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LogoutSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            refresh_token = serializer.validated_data['refresh']
            try:
                refresh_token.blacklist()
                return Response(
                    {
                        "message": "Logout successful.",
                        "result": {}
                    },
                    status=status.HTTP_200_OK
                )
            except TokenError:
                return Response(
                    {
                        "message": "Invalid or expired refresh token.",
                        "result": {}
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response(
            {
                "message": "Validation error",
                "result": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )