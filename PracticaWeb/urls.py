"""PracticaWeb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from django.contrib.auth.views import LoginView,LogoutView
from rest_framework import routers
from forkilla import views

router = routers.DefaultRouter()
router.register(r'restaurants',views.RestaurantViewSet, basename="restaurant")
router.register(r'reviews', views.ReviewViewSet, basename="review")


urlpatterns = [
	url(r'^forkilla/', include('forkilla.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/login/$', LoginView.as_view(template_name='registration/login.html'), name ='login'),
    url(r'^accounts/logout/$', LogoutView.as_view(template_name='registration/logged_out.html'), {'next_page': '/'} ,name='logout'),
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'', include('forkilla.urls')),

]

handler404 ='forkilla.views.handler404'
handler500 ='forkilla.views.handler500'