from django.contrib import admin

# Register your models here.
# admin.py
from django.contrib import admin
from .models import Director, Movie, Review


@admin.register(Director)
class DirectorAdmin(admin.ModelAdmin):
    pass


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    pass


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    pass
