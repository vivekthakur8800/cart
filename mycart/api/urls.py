from django.urls import path
from api.views import SendPasswordResetEmailView, UserLoginView, UserProfileView, UserRegistrationView,UserChangePasswordView,UserPasswordResetView,CustomerAPI,ProductAPI,CartAPI,OrderPlacedAPI
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView,TokenVerifyView

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('register/',UserRegistrationView.as_view(),name='register'),
    path('userlogin/',UserLoginView.as_view(),name='userlogin'),
    path('userprofile/',UserProfileView.as_view(),name='userprofile'),
    path('changepassword/',UserChangePasswordView.as_view(),name='changepassword'),
    path('send-password-reset-email/',SendPasswordResetEmailView.as_view(),name='send-password-reset-email'),
    path('reset-password/<uid>/<token>/',UserPasswordResetView.as_view(),name='rest-password'),
    path('customerapi/',CustomerAPI.as_view(),name='customerapi'),
    path('customerapi/<int:pk>/',CustomerAPI.as_view(),name='customerapi'),
    path('productapi/',ProductAPI.as_view(),name='productapi'),
    path('productapi/<int:pk>/',ProductAPI.as_view(),name='productapi'),
    path('cartapi/',CartAPI.as_view(),name='cartapi'),
    path('cartapi/<int:pk>/',CartAPI.as_view(),name='cartapi'),
    path('orderplacedapi/',OrderPlacedAPI.as_view(),name='orderplacedapi'),
    path('orderplacedapi/<int:pk>/',OrderPlacedAPI.as_view(),name='orderpalcedapi'),
]