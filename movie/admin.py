from django.contrib import admin
from .models import Movie,Review

# Register your models here.
# class BookAdmin(admin.ModelAdmin):
#     list_display = ('id','title', 'description')

admin.site.register(Movie)
admin.site.register(Review)