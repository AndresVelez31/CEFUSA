from django.contrib import admin
from .models import LandingPage, LandingSlide


class LandingSlideInline(admin.TabularInline):
	model = LandingSlide
	extra = 1


@admin.register(LandingPage)
class LandingPageAdmin(admin.ModelAdmin):
	list_display = ('title', 'updated_at')
	inlines = [LandingSlideInline]


@admin.register(LandingSlide)
class LandingSlideAdmin(admin.ModelAdmin):
	list_display = ('title', 'section', 'order', 'active')
	list_filter = ('section', 'active')
	ordering = ('section', 'order')
