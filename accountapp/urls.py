from django.urls import include, path
from .views import LoginAPIView, LogoutAPIView,UserRegisterAPIView, AdminRegisterAPIView,UserAPIView

urlpatterns = [
    path("register/user/", UserRegisterAPIView.as_view(), name="user-register"),
    path("register/admin/", AdminRegisterAPIView.as_view(), name="admin-register"),
    path('login/', LoginAPIView.as_view()),
    path('user/', UserAPIView.as_view()),
    path('logout/', LogoutAPIView.as_view()),

]