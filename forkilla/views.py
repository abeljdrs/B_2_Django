from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Restaurant, ViewedRestaurants, RestaurantInsertDate, Reservation ,Review
from .forms import ReservationForm, ReviewForm
from django.urls import reverse
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login, authenticate
from datetime import datetime
from django.contrib.auth.models import User,Group
from rest_framework import viewsets
from .serializers import RestaurantSerializer, ReviewSerializer
from .permission import IsCommercialOrReadOnly
from rest_framework import status
from rest_framework import permissions
from rest_framework.views import APIView







# Create your views here.

def index(request):
	promoted_restaurants = []
	promoted_restaurants = Restaurant.objects.filter(is_promot="True")
	cities = Restaurant.objects.order_by('city').values('city').distinct()
	cities_ok = []
	for city in cities:
		cities_ok.append(city.get('city'))

	
	
	names = []
	for resto in promoted_restaurants:
		names.append(resto.name)
	context = {
		"restaurantes": promoted_restaurants,
		"cities": cities_ok,
		'viewedrestaurants':_check_session(request),
	}
	return render(request, 'forkilla/homePage.html',context)




def restaurants(request, city="", category=""):
	print("negroooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo")
	promoted = False

	if city:
		restaurants_by_city = Restaurant.objects.filter(city__iexact=city)
		if category:
			restaurants_by_city = Restaurant.objects.filter(city__iexact=city,category__iexact=category)
	else:
		restaurants_by_city = Restaurant.objects.all()
		promoted= True

	context = {
		'city': city,
		'restaurants': restaurants_by_city,
		'promoted': promoted,
		'viewedrestaurants':_check_session(request),

	}
	return render(request, 'forkilla/restaurants.html',context)


def _check_session(request):
		if "viewedrestaurants" not in request.session:
			viewedrestaurants = ViewedRestaurants()
			viewedrestaurants.save()
			request.session["viewedrestaurants"] = viewedrestaurants.id_vr
		else:
			viewedrestaurants = ViewedRestaurants.objects.get(id_vr=request.session["viewedrestaurants"])
		return viewedrestaurants


def details(request, rest_detail=""):


	try:
		if request.method == "POST":
			form = ReviewForm(request.POST)
			if form.is_valid():
				opinion = form.save(commit=False)
				restaurant_number = rest_detail
				opinion.rest_number = restaurant_number
				opinion.review_user = request.user.username
				opinion.save()

										
			else:
				request.session["result"] = form.errors


			context = {
				'restaurant':Restaurant.objects.get(restaurant_number = rest_detail),
				'viewedrestaurants':_check_session(request),
				'form':'null',
				'reviews':Review.objects.filter(rest_number = rest_detail),
			}	
			return render(request, 'forkilla/details.html', context)
			


		elif request.method == "GET":
			viewedrestaurants = _check_session(request)
			restaurant = Restaurant.objects.get(restaurant_number = rest_detail)
			lastviewed = RestaurantInsertDate(viewedrestaurants = viewedrestaurants, restaurant = restaurant)
			lastviewed.save()
			restaurant_number = rest_detail
			restaurant = Restaurant.objects.get(restaurant_number = restaurant_number)
			request.session["reserved_restaurant"] = restaurant_number
			form = ReviewForm()
			context = {
				'restaurant':restaurant,
				'viewedrestaurants':_check_session(request),
				'form':form,
				'reviews':Review.objects.filter(rest_number = rest_detail),

			}

			return render(request, 'forkilla/details.html', context)
	except Restaurant.DoesNotExist:
		return HttpResponse("Restaurant Does Not Exists")




def reservation(request):
	try:
		if request.method == "POST":
			form = ReservationForm(request.POST)
			if form.is_valid():
				resv = form.save(commit=False)
				time = resv.time_slot
				day = resv.day
				people = resv.num_people

				
				context = {
					'reservation':"",
					'viewedrestaurants':_check_session(request),
				}


				print("tiempoooooooooooooooooo"+str(time))

				
				restaurant_number = request.session["reserved_restaurant"]
				resv.restaurant = Restaurant.objects.get(restaurant_number = restaurant_number)
				resv.reservation_user = request.user.username
				
				request.session["reservation"] = resv.id
				request.session["result"] = "OK"
				
				print("_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/")
				ocupacion = Reservation.objects.values_list('num_people',flat=True).filter(time_slot = time,restaurant = resv.restaurant,day = day )
				suma_ocup = sum(ocupacion)
				print(ocupacion)
				print(suma_ocup)
				capacidad_total = Restaurant.objects.values_list('capacity',flat=True).get(restaurant_number = restaurant_number)

				if (capacidad_total >= suma_ocup+resv.num_people):
					print("reservadooooooooooooooooooooooooooooooooooooooooo")
					
					context['reservation']="Realizada correctamente"
					resv.save()
					
				else:
					print("canceladooooooooooooooooooooooooooooooooooooooooo")
					context['reservation']="Error en la reserva"
					
					
			else:
				request.session["result"] = form.errors



			return render(request, 'forkilla/checkout.html',context)

		elif request.method == "GET":
			restaurant_number = request.GET["reservation"]
			restaurant = Restaurant.objects.get(restaurant_number = restaurant_number)
			request.session["reserved_restaurant"] = restaurant_number

			form = ReservationForm()
			context = {
				'restaurant': restaurant,
				'form': form,
				'viewedrestaurants':_check_session(request),

			}
	except Restaurant.DoesNotExist:
		return HttpResponse("Restaurant Does Not Exists")

	return render(request, 'forkilla/reservation.html',context)



def checkout(request):


	return render(request, 'forkilla/checkout.html',context)


def searchByCity(request):

	city = request.GET.get('q','')
	print("blancooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo")



	return restaurants(request,city=city)


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect(reverse("index"))
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {
        'form': form,
    })


	
def logout(request):
	logout(request)

def login(request):
	username = request.POST['username']
	password = request.POST['password']
	user = authenticate(request, username=username, password=password)
	if user is not None:
		login(request,user)


def handler404(request, *args, **argv):
    return render(request, 'forkilla/404.html', status=404)


def handler500(request, *args, **argv):
    return render(request, 'forkilla/500.html', status=500)


def comparator(request):
	return render(request,'forkilla/comparator.html')


@login_required
def reservationList(request):
	if request.method == "POST":
		print("post")
		idReserva = request.POST['reservation']
		Reservation.objects.filter(id=idReserva).delete()
		username = request.user.username
		reservas = Reservation.objects.filter(reservation_user = username)
		resv_compared = []
		for reserva in reservas:
			if datetime.now().date() > reserva.day:
				resv_compared.append([reserva,'old'])
			else:
				resv_compared.append([reserva,'future'])

		context = {
			'user':username,
			'reservas':resv_compared,
		}

		return render(request,'forkilla/reservationList.html',context)
		
			

	elif request.method == "GET":
		username = request.user.username
		reservas = Reservation.objects.filter(reservation_user = username)
		resv_compared = []
		for reserva in reservas:
			if datetime.now().date() > reserva.day:
				resv_compared.append([reserva,'old'])
			else:
				resv_compared.append([reserva,'future'])

		context = {
			'user':username,
			'reservas':resv_compared,
		}
		return render(request,'forkilla/reservationList.html',context)




def review(request,rest_num,id_resv):

	if request.method == "POST":
			form = ReviewForm(request.POST)
			if form.is_valid():
				opinion = form.save(commit=False)
				restaurant_number = rest_num
				opinion.rest_number = restaurant_number
				opinion.review_user = request.user.username
				opinion.save()
				Reservation.objects.filter(id = id_resv).delete()
			else:
				request.session["result"] = form.errors
				

			next = request.POST.get('next','/')


			return HttpResponseRedirect( next)
			


	elif request.method == "GET":
		viewedrestaurants = _check_session(request)
		restaurant = Restaurant.objects.get(restaurant_number = rest_num)
		lastviewed = RestaurantInsertDate(viewedrestaurants = viewedrestaurants, restaurant = restaurant)
		lastviewed.save()
		restaurant_number = rest_num
		restaurant = Restaurant.objects.get(restaurant_number = restaurant_number)
		form = ReviewForm()
		context = {
			'restaurant':restaurant,
			'viewedrestaurants':_check_session(request),
			'form':form,
			'ruta':request.META.get('HTTP_REFERER'),
		}

		return render(request, 'forkilla/review.html', context)

class RestaurantViewSet(viewsets.ModelViewSet):
	serializer_class = RestaurantSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsCommercialOrReadOnly)
	
	def get_queryset(self):
		queryset = Restaurant.objects.all()
		
		category = self.request.query_params.get('category', None)
		if category is not None:
			queryset = queryset.filter(category=category)
		city = self.request.query_params.get('city', None)
		if city is not None:
			queryset = queryset.filter(city=city)
		price = self.request.query_params.get('price', None)
		if price is not None:
			queryset = queryset.filter(price_average__lte=price)

		return queryset
	

class ReviewViewSet(viewsets.ModelViewSet):
	serializer_class = ReviewSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsCommercialOrReadOnly)

	def get_queryset(self):
		return Review.objects.all()
	




	
	



	








	