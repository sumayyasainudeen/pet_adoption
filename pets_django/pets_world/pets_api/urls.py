from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.ok, name = 'ok'),
    path('register/',views.register_view , name="register_view"),
    path('login/',views.login_view , name="login_view"),
    path('donorlist/',views.get_donor_list , name="get_donor_list"),
    path('deletedonor/<int:id>/', views.delete_donor, name='delete_donor'),
    path('userlist/', views.get_user_list, name='get_user_list'),
    path('addcategory/', views.add_category, name='add_category'),
    path('getcategories/', views.get_categories, name='get_categories'),
    path('deletecategory/', views.delete_category, name='delete_category'),
    path('deletecategory/<int:id>/', views.delete_category, name='delete_category'),

    path('donatepet/', views.donate_pet, name='donate_pet'),
    path('getdonationrequests/', views.get_donation_requests, name='get_donation_requests'),


]
