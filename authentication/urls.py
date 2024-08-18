from django.urls import path

from .views import RegisterUserView
urlpatterns = [
    path('register/', view=RegisterUserView.as_view(), name='register')
]
