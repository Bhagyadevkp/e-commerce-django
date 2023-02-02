from django.contrib import admin
from  . models import *
# Register your models here.
# #

class catelogAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

admin.site.register(catelog,catelogAdmin)


class prodAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('prod_id',)}
    list_display = ['name','slug','user','title','category','subcategory']
admin.site.register(additems,prodAdmin)


admin.site.register(merchshop)


class subcatelogAdmin(admin.ModelAdmin):
    list_display = ['subcategoryname','maincategoryname']
admin.site.register(subcatelog, subcatelogAdmin)





