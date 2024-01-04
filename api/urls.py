from django.urls import path

from . import views

urlpatterns=[
    path('',views.SignUpView.as_view()),
    path('sign_in',views.SignInView.as_view()),
    path('wallet/<int:pk>',views.Wallet.as_view()),
    path('deposit', views.Deposit.as_view()),
    path('withdrawal',views.Withdraw.as_view())
]