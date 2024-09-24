from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path
from api import views

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='api_token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='api_token_refresh'),

    path('api/assets/', views.AssetsListView.as_view(), name='api_assets_list'),
    path('api/transactions/', views.TransactionsListView.as_view(), name='api_transactions_list'),
    path('api/transactions/create/', views.TransactionCreateView.as_view(), name='api_transaction_create'),
    path('api/transactions/update/<int:id>/', views.TransactionUpdateView.as_view(), name='api_transaction_update'),
    path('api/transactions/delete/<int:id>/', views.TransactionDeleteView.as_view(), name='api_transaction_delete'),
]