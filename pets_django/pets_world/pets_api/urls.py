from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
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
    path('approvedonationrequest/<int:id>/', views.approve_donation_request, name='approve_donation_request'),
    path('canceldonationrequest/<int:id>/', views.cancel_donation_request, name='cancel_donation_request'),

    path('getcategorywisedata/<int:id>/', views.get_category_wise_data, name='get_category_wise_data'),
    path('adoptpet/', views.adopt_pet, name='adopt_pet'),
    path('getdonornotifications/', views.get_donor_notifications, name='get_donor_notifications'),
    path('handledonornotification/<int:id>/', views.handle_donor_notification, name='handle_donor_notification'),
    path('getnotificationcount/', views.get_notification_count, name='get_notification_count'),
    path('updatepassword/', views.update_password, name='update_password'),
    path('getpurchasedetails/<int:id>/', views.get_purchase_details, name='get_purchase_details'),
    path('getdonationdetails/<int:id>/', views.get_donation_details, name='get_donation_details'),

    path('deletepet/<int:id>/', views.delete_pet, name='delete_pet'),
    path('getprofiledata/', views.get_profile_data, name='get_profile_data'),
    path('updateprofiledata/', views.update_profile_data, name='update_profile_data'),
    path('getadoptedpets/', views.get_adopted_pets, name='get_adopted_pets'),
    path('getdonatedpets/', views.get_donated_pets, name='get_donated_pets'),


]
