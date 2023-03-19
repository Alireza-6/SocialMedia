from django.core.validators import MinLengthValidator
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers, status

from users.models import BaseUser, Profile
from users.selectors import get_profile
from users.services import register
from users.validators import letter_validator, number_validator, special_character_validator


class ProfileApi(APIView):
    class GetProfileOutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Profile
            exclude = ["user"]

    @extend_schema(responses=GetProfileOutputSerializer)
    def get(self, request):
        res = get_profile(user=request.user)
        return Response(
            self.GetProfileOutputSerializer(res, context={"request": request}, many=True).data,
            status=status.HTTP_200_OK
        )


class RegisterApi(APIView):
    class RegisterInputSerializer(serializers.Serializer):
        email = serializers.EmailField()
        bio = serializers.CharField(max_length=1000, required=False)
        password = serializers.CharField(
            validators=[
                letter_validator,
                number_validator,
                special_character_validator,
                MinLengthValidator(limit_value=10)
            ]
        )
        confirm_password = serializers.CharField(max_length=255)

        def validate_email(self, email):
            if BaseUser.objects.filter(email=email).exists():
                raise serializers.ValidationError("Email Already Token")
            return email

        def validate(self, data):
            if not data.get("password") or not data.get("confirm_password"):
                raise serializers.ValidationError("Please Fill Password And Confirm Password")

            if data.get("password") != data.get("confirm_password"):
                raise serializers.ValidationError("Password Is Not Equal To Confirm Password")
            return data

    class RegisterOutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = BaseUser
            fields = ["email", "created_at", "updated_at"]

    @extend_schema(request=RegisterInputSerializer, responses=RegisterOutputSerializer)
    def post(self, request):
        payload = self.RegisterInputSerializer(data=request.data)
        payload.is_valid(raise_exception=True)
        try:
            res = register(
                email=payload.validated_data.get("email"),
                password=payload.validated_data.get("password"),
                bio=payload.validated_data.get("bio"),
            )
        except Exception as ex:
            Response(f"Database Error {ex}", status=status.HTTP_400_BAD_REQUEST)
        return Response(
            self.RegisterOutputSerializer(res, context={"request": request}).data, status=status.HTTP_201_CREATED
        )
