from django.urls import path
from . import views


urlpatterns=[
    path('',views.first,name='first'),

    path('add/<int:id>/<str:name>/<str:subcategoryname>',views.add,name='add'),
    path('addshop',views.addshop,name='addshop'),
    # path('extshop',views.extshop,name='extshop'),
    path('detailprod/<int:id>',views.detailprod,name='detailprod'),
    path('filter/<str:name>',views.filter,name='filter'),
    path('myorders',views.myorders,name='myorders'),
    path('ordersplaced',views.ordersplaced,name='ordersplaced'),
    path('singleproductdetail/<int:id>',views.singleproductdetail,name='singleproductdetail'),
    path('search', views.search, name='search'),
    path('searchproduct', views.searchproduct, name='searchproduct'),
    path('searchlocation', views.searchlocation, name='searchlocation'),
    path('categcreation/<int:id>',views.categcreation,name='categcreation'),
    path('extexp', views.extexp, name='extexp'),
# path('subcategcreation/<int:id>/<str:name>/',views.subcategcreation,name='subcategcreation'),

    path('profile2', views.profile2, name='profile2'),
]