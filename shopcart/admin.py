from django.contrib import admin

# Register your models here.
from shopcart.models import cart, cartitems, buy

admin.site.register(cart)
admin.site.register(cartitems)
class buyAdmin(admin.ModelAdmin):

    list_display = ['productname','username','sellinguser','shopname','quantity']
admin.site.register(buy,buyAdmin)
