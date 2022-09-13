from django.urls import path

from . import views

app_name = 'items'


urlpatterns = [
    path('buy/<int:id>/', views.BuyView.as_view(), name='buy_item'),
    path('item/<int:id>/', views.ItemView.as_view(), name='get_item'),
    path(
        'check_order/<int:id>/',
        views.OrderView.as_view(),
        name='check_order'
    ),
    path(
        'pay_for_order/<int:id>/',
        views.PayForOrderVew.as_view(),
        name='pay_for_order'
    ),
    path('success/', views.SuccessView.as_view(), name='success_payment'),
    path('cancel/', views.CancelView.as_view(), name='failed_payment'),
]
