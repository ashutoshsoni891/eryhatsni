from django.urls import path, include
from . import views

urlpatterns = [
    path('v1/registerUser/', views.registerUser),
    path('v1/addContacts/', views.addContacts),
    path('v1/searchUser/', views.searchUser),
    path('v1/markSpamByID/', views.markSpamByID)
]