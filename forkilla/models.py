from django.db import models
from datetime import datetime
from django.core.validators import MinValueValidator
from django.core.validators import MaxValueValidator
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from pygments import highlight


# Create your models here.
class Restaurant(models.Model):
	CATEGORIES = (
		("Rice", "Rice"),
        ("Fusi", "Fusion"),
        ("BBQ", "Barbecue"),
        ("Chin", "Chinese"),
        ("Medi","Mediterranean"),
        ("Crep","Creperie"),
        ("Hind","Hindu"),
        ("Japa","Japanese"),
        ("Ital","Italian"),
        ("Mexi","Mexican"),
        ("Peru", "Peruvian"),
        ("Russ","Russian"),
        ("Turk","Turkish"),
        ("Basq","Basque"),
        ("Vegy", "Vegetarian"),
        ("Afri","African"),
        ("Egyp","Egyptian"),
        ("Grek","Greek")
	)

	_d_categories = dict(CATEGORIES)

	restaurant_number = models.CharField(max_length=8, unique=True)
	name = models.CharField(max_length=50)
	menu_description = models.TextField()
	price_average = models.DecimalField(max_digits=5, decimal_places=2)
	is_promot = models.BooleanField()
	rate = models.DecimalField(max_digits=3, decimal_places=1)
	address = models.CharField(max_length=50)
	city = models.CharField(max_length=50)
	country = models.CharField(max_length=50)
	featured_photo = models.ImageField(upload_to="photo_dir")
	category = models.CharField(max_length=5,choices = CATEGORIES)
	capacity = models.PositiveIntegerField()
   

	def get_human_category(self):
		return self._d_categories[self.category]

	def __str__(self):
		return ("[**Promoted**]" if self.is_promot else " ") + "[" + self.category+"] " \
				"["+self.restaurant_number + "] "+ self.name + " - "+ self.menu_description + " (" + str(self.rate) + ")" \
				": " + str(self.price_average) + u" €"




class Reservation(models.Model):
    
    SLOTS = (
        ("morning_first", "12h00"),
        ("morning_second", "13h00"),
        ("morning_third", "14h00"),
        ("morning_fourth", "15h00"),
        ("evening_first", "20h00"),
        ("evening_second", "21h00"),
        ("evening_third", "22h00"),
    )
    _d_slots = dict(SLOTS)
    id = models.AutoField(primary_key=True)
    day = models.DateField(default=datetime.now)
    time_slot = models.CharField(max_length=15, choices=SLOTS)
    num_people = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    reservation_user = models.CharField(max_length=50, default='')
    restaurant = models.ForeignKey(
        'Restaurant',
        on_delete = models.CASCADE,
    )


    def get_human_slot(self):
        return self._d_slots[self.time_slot]

    def get_all_reservations(self):
        return self.objects.all()

    def __str__(self):
        return (str(self.restaurant.name)+" "+str(self.day)+" - at "+ str(self.time_slot) +" - for "+str(self.num_people)+ " persons")


class ViewedRestaurants(models.Model):
    id_vr = models.AutoField(primary_key=True)
    restaurant = models.ManyToManyField(Restaurant, through='RestaurantInsertDate')

class RestaurantInsertDate(models.Model):
    viewedrestaurants = models.ForeignKey(ViewedRestaurants, on_delete = models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete = models.CASCADE)
    date_added = models.DateTimeField(auto_now_add = True)

class Meta:
    ordering = ['-date_added']




class Review(models.Model):
    id = models.AutoField(primary_key=True)
    stars = models.PositiveIntegerField(
            default=1,
            validators=[MaxValueValidator(5),MinValueValidator(1)]
        )
    comment = models.CharField(max_length=280)
    review_user = models.CharField(max_length=50)
    rest_number = models.CharField(max_length=8)

    def __str__(self):
        return (str(self.review_user)+" "+str(self.rest_number))











