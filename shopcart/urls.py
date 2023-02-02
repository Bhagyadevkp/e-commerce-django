from django.urls import  path
from . import views

urlpatterns=[
    path('cartdetails',views.cartdetails,name='cartdetails'),
    path('cartitemsadded/<int:id>/<str:shopname>',views.cartitemsadded,name='cartitemsadded'),
    path('addquan/<int:id>', views.addquan, name='addquan'),
    path('lessquan/<int:id>', views.lessquan, name='lessquan'),
    path('checkout', views.checkout, name='checkout'),
    path('purchase',views.purchase,name='purchase'),
    path('remove/<int:id>', views.remove, name='remove'),

]