from django.urls import path, re_path
from dj_rest_auth.registration.views import RegisterView, VerifyEmailView, ConfirmEmailView, ResendEmailVerificationView
from dj_rest_auth.views import LoginView, LogoutView, PasswordChangeView, PasswordResetView, PasswordResetConfirmView, UserDetailsView

urlpatterns = [    
    # Returns current user
    path('user/', UserDetailsView.as_view(), name='user_details'),
    
    # Authentication        
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('password/change/', PasswordChangeView.as_view(), name='password_change'),        

    # Registration urls
    path('registration/account-confirm-email/<str:key>/', ConfirmEmailView.as_view(), name='account_confirm_email'),
    path('registration/', RegisterView.as_view()),
    path('registration/verify-email/', VerifyEmailView.as_view(), name='account_email_verification_sent'),
    path('registration/resend-email', ResendEmailVerificationView.as_view(), name='resend-email'),
    
    # Reset password
    path('password/reset/', PasswordResetView.as_view()),
    path('password/reset/confirm/<slug:uidb64>/<slug:token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),    
]