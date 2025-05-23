from django.urls import path

from . import views

urlpatterns = [
    path("", views.cart_detail, name="cart_detail"),
    path("<product_slug>/add", views.add_cart, name="add_cart"),
    path("<product_slug>/remove", views.remove_cart, name="remove_cart"),
    #path('cart/', views.cart_view, name='cart')

    #path("remove/<slug:product_slug>/", views.remove_cart, name="remove_cart"),

]
