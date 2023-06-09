from django.contrib import admin

# Register your models here.
from .models import  person , property
 
admin.site.register(property)
admin.site.register(person)

