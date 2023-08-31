from django.contrib.auth import get_user_model
from rest_framework import views, status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from user.serializers import UserSerializer


class RegisterView(views.APIView):
    http_method_names = ["post"]

    def post(self, *args, **kwargs) -> Response:
        serializer = UserSerializer(data=self.request.data)
        if serializer.is_valid():
            get_user_model().objects.create_user(**serializer.validated_data)
            return Response(status=status.HTTP_201_CREATED)
        return Response(
            status=status.HTTP_400_BAD_REQUEST,
            data={"errors": serializer.errors},
        )


class RetrieveUpdateUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self) -> get_user_model():
        return self.request.user
