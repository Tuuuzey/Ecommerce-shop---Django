from rest_framework import viewsets
from shop.models import Products
from ..serializers.serializer_products import ProductsSerializer
from drf_spectacular.utils import extend_schema, OpenApiParameter

class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API for managing products. Allows retrieving a list of products and individual product details.
    """
    queryset = Products.objects.all()
    serializer_class = ProductsSerializer
    lookup_field = 'id'

    @extend_schema(
        summary="Retrieve Product List",
        description="Returns a list of all available products.",
        responses={200: ProductsSerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Retrieve Product Details",
        description="Returns details of a specific product based on its ID.",
        parameters=[
            OpenApiParameter(name="id", description="Product ID", required=True, type=int)
        ],
        responses={200: ProductsSerializer},
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
