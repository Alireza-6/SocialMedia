from drf_spectacular.utils import extend_schema
from rest_framework import status, serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from blog.models import Subscription
from blog.selectors import get_subscribers
from blog.services import unsubscribe, subscribe
from core.mixins import ApiAuthMixin


class SubscribeDetailApi(ApiAuthMixin, APIView):
    def delete(self, request, email):
        try:
            unsubscribe(user=request.user, email=email)
        except Exception as ex:
            return Response({"detail": "Database Error - " + str(ex)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)


class SubscribeApi(ApiAuthMixin, APIView):
    class InputSubSerializer(serializers.Serializer):
        email = serializers.CharField(max_length=100)

    class OutPutSubSerializer(serializers.ModelSerializer):
        email = serializers.SerializerMethodField("get_email")

        class Meta:
            model = Subscription
            fields = ("email",)

        def get_email(self, subscription):
            return subscription.target.email

    @extend_schema(responses=OutPutSubSerializer)
    def get(self, request):
        user = request.user
        query = get_subscribers(user=user)
        return Response(self.OutPutSubSerializer(query, context={"request": request}).data)

    @extend_schema(request=InputSubSerializer, responses=OutPutSubSerializer)
    def post(self, request):
        serializer = self.InputSubSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            query = subscribe(user=request.user, email=serializer.validated_data.get("email"))
        except Exception as ex:
            return Response({"detail": "Database Error - " + str(ex)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(self.OutPutSubSerializer(query).data)
