from django.contrib import admin
from .models import * 


# class categoryadmin(admin.ModelAdmin):
#     list_display = ('name','image','description')

admin.site.register(Category)
admin.site.register(Product)
