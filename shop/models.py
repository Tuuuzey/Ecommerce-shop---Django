from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from seller.models import SellerUser
from django.contrib.auth.models import User
from django.db.models import Avg
from math import floor


# Create your models here.
class Products(models.Model):
    CATEGORY_CHOICES = [
        ('electronics', 'Electronics'),
        ('fashion', 'Fashion & Clothing'),
        ('home_garden', 'Home & Garden'),
        ('health_beauty', 'Health & Beauty'),
        ('toys', 'Toys & Kids'),
        ('sports', 'Sports & Recreation'),
        ('automotive', 'Automotive'),
        ('supermarket', 'Supermarket'),
        ('books', 'Books & Media'),
        ('pets', 'Pets'),
        ('office_school', 'Office & School Supplies'),
    ]
    name = models.CharField(max_length=255, null=False)
    price = models.FloatField(validators=[MinValueValidator(0.00), MaxValueValidator(99999.99)])
    discount_price = models.FloatField(validators=[MinValueValidator(0.00), MaxValueValidator(99999.99)], null=True, blank=True)
    category = models.CharField(max_length=255, choices=CATEGORY_CHOICES, null=False)
    description = models.TextField(null=False)
    image = models.CharField(max_length=700)
    stripe_price_id = models.CharField(max_length=255, unique=True, null=True, blank=True)
    stock = models.BooleanField(default=True, null=True)
    seller = models.ForeignKey(SellerUser, on_delete=models.CASCADE, related_name='products')
    opinion = models.FloatField(validators=[MinValueValidator(0.00), MaxValueValidator(5.00)], null=True, blank=True)

    def __str__(self):
        return self.name
    
    def get_average_rating(self):
        comments = Comment.objects.filter(order_item__product=self, rating__isnull=False)
        avg = comments.aggregate(average=Avg('rating'))['average']
        return avg if avg is not None else 0


    @property
    def average_rating(self):
        return self.get_average_rating()
    
    def get_rating_count(self):
        comments = Comment.objects.filter(order_item__product=self, rating__isnull=False)
        return comments.count()

    @property
    def rating_count(self):
        return self.get_rating_count()
    
    @property
    def stars_data(self):
        average = self.average_rating
        full_stars = floor(average)
        half_star = 1 if average % 1 >= 0.5 else 0 
        empty_stars = 5 - full_stars - half_star

        return {
            'full_stars': full_stars,
            'half_star': half_star,
            'empty_stars': empty_stars,
        }



class ProductImage(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='images')
    image_url = models.CharField(max_length=700)

    def __str__(self):
        return f"Image for {self.product.name}"
    
class Comment(models.Model):
    order_item = models.ForeignKey('checkout.OrderItem', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    rating = models.DecimalField(max_digits=2, decimal_places=1, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment on {self.order_item.product.name} from Order {self.order_item.order.id}'
