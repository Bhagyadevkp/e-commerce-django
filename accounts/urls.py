from django.urls import path,include


from . import views
from .views import verificationView, loginView,changepassword


urlpatterns=[
    path('register',views.register,name='register'),
    # path('login', views.login, name='login'),
    path('loginned', loginView.as_view(), name='loginned'),
    path('logout',views.logout,name='logout'),
    # path('merchant',views.merchant,name='merchant'),
    path('profile',views.profile,name='profile'),
    path('detailshop/<str:shopname>',views.detailshop,name='detailshop'),
    path('update/<int:id>',views.update,name='update'),
    path('delete/<int:id>',views.delete,name='delete'),
    path('activate/<uidb64>/<token>',verificationView.as_view(),name='activate'),

    path('stock_finished/<int:id>',views.stock_finished,name='stock_finished'),
    path('ext_date/<int:id>',views.ext_date,name='ext_date'),
    path('edit_shop/<int:id>',views.edit_shop,name='edit_shop'),
    path('delete_shop/<int:id>',views.delete_shop,name='delete_shop'),
    path('pendingdelivery/<int:id>', views.pendingdelivery, name='pendingdelivery'),
    path('forgetpassword',views.forgetpassword,name='forgetpassword'),
    path('changepassword/<uidb64>/<token>', changepassword.as_view(), name='changepassword'),
    # path('checkpassword',views.checkpassword,name='checkpassword'),
]