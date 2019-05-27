from .models import Restaurant, Review
from rest_framework import serializers

class RestaurantSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Restaurant
		fields = ('url',	
        'restaurant_number', 'name', 'menu_description', 
		'price_average', 'is_promot', 'rate', 'address', 
		'city', 'country', 'featured_photo', 'category', 
		'capacity')
		
class ReviewSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Review
		fields = (
		'url', 'stars', 'comment', 'review_user', 'rest_number')