from django.urls import path

from .views import RegisterUserView, LoginUserView
urlpatterns = [
    path('register/', view=RegisterUserView.as_view(), name='register'),
    path('login/', view=LoginUserView.as_view(), name='login')
]
