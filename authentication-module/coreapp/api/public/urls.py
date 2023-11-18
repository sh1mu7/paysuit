from django.urls import path

from . import views

urlpatterns = [
    path('country/', views.CountryAPI.as_view()),
    path('signup/', views.SignupAPI.as_view(), name='signup'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('login/2fa/', views.Login2FAView.as_view(), name='login-2fa'),
    path('delete/', views.DeleteAccountAPI.as_view(), name='delete-account'),
    path('profile/', views.ProfileAPI.as_view(), name='profile'),
    path('verification/resend/', views.ResendVerificationAPI.as_view(), name='resend-verification'),
    path('verification/check/', views.OTPCheckAPI.as_view(), name='otp-check'),
    path('account/verify/', views.AccountVerifyAPI.as_view(), name='account-verify'),
    path('change/password/', views.PasswordChangeAPI.as_view(), name='change-password'),
    path('forget/password/', views.ForgetPasswordAPI.as_view(), name='forget-password'),
    path('forget/password/confirm/', views.ForgetPasswordConfirmAPI.as_view(), name='forget-password-confirm'),
    path('setup/2fa/', views.Setup2FAAPI.as_view(), name='setup-2fa'),
    # path('documents/upload/', views.UploadDocumentsAPI.as_view(), name='forget-password-confirm'),
]
