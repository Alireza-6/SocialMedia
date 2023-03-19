from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers, status

from blog.models import Product
from blog.selectors import get_products
from blog.services import create_product


class ProductApi(APIView):
    class CreateProductInputSerializer(serializers.Serializer):
        name = serializers.CharField(max_length=255)

    class CreateProductOutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Product
            fields = "__all__"

    @extend_schema(request=CreateProductInputSerializer, responses=CreateProductOutputSerializer)
    def post(self, request):
        payload = self.CreateProductInputSerializer(data=request.data)
        payload.is_valid(raise_exception=True)
        try:
            res = create_product(name=payload.validated_data.get("name"))
        except Exception as ex:
            Response(f"Database Error {ex}", status=status.HTTP_400_BAD_REQUEST)
        return Response(
            self.CreateProductOutputSerializer(res, context={"request": request}).data, status=status.HTTP_201_CREATED
        )

    def get(self, request):
        res = get_products()
        return Response(
            self.CreateProductOutputSerializer(res, context={"request": request}, many=True).data,
            status=status.HTTP_200_OK
        )
