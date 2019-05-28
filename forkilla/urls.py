from django.conf.urls import url

from django.conf import settings
from django.conf.urls.static import static

from . import views

listOfAddresses = ['https://sd2019-forkillaa7.herokuapp.com']
urlpatterns = [
	url(r'^register/$', views.register, name='register'),
	url(r'^comparator/$', views.comparator, name='comparator'),
	url(r'^$', views.index, name = 'index'),
	url(r'^restaurants/$', views.restaurants, name='restaurants'),
	url(r'^restaurants/(?P<city>.*)/(?P<category>.*)$', views.restaurants, name='restaurants'),
	url(r'^restaurants/(?P<city>.*)/$', views.restaurants, name='restaurants'),
	url(r'^restaurant/(?P<rest_detail>.*)/$', views.details, name="details"),
	url(r'^reservation/checkout/$', views.checkout, name='checkout'),
	url(r'^reservation/$', views.reservation, name='reservation'),
	url(r'^reservationlist/$', views.reservationList, name='reservationlist'),
	url(r'^reservationlist/review/(?P<rest_num>.*)/(?P<id_resv>.*)$', views.review, name='review'),
	url(r'^search/$', views.searchByCity, name="searchByCity"),
	

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)