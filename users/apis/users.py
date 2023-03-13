from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers, status

from users.models import BaseUser
from users.services.users import create_user


class RegisterApi(APIView):
    class InputSerializer(serializers.Serializer):
        email = serializers.EmailField()
        password = serializers.CharField(max_length=255)
        confirm_password = serializers.CharField(max_length=255)

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = BaseUser
            fields = ["email"]

    def post(self, request):
        payload = self.InputSerializer(data=request.data)
        payload.is_valid(raise_exception=True)
        try:
            res = create_user(
                email=payload.validated_data.get("email"),
                password=payload.validated_data.get("password"),
            )
        except Exception as ex:
            Response(f"Database Error {ex}", status=status.HTTP_400_BAD_REQUEST)
        return Response(self.OutputSerializer(res, context={"request": request}).data, status=status.HTTP_201_CREATED)
