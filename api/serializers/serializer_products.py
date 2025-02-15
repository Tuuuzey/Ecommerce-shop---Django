from rest_framework import serializers
from shop.models import Products, ProductImage, Comment

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['image_url']

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    
    class Meta:
        model = Comment
        fields = ['user', 'content', 'rating', 'created_at']

class ProductsSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True) 
    comments = CommentSerializer(source='order_item_set', many=True, read_only=True)
    average_rating = serializers.FloatField(source='get_average_rating', read_only=True) 
    rating_count = serializers.IntegerField(source='get_rating_count', read_only=True) 
    stars_data = serializers.SerializerMethodField()

    class Meta:
        model = Products
        fields = ['id', 'name', 'price', 'discount_price', 'category', 'description', 'image', 'stock', 'seller',
                  'average_rating', 'rating_count', 'stars_data', 'images', 'comments']
    
    def get_stars_data(self, obj):
        return obj.stars_data
