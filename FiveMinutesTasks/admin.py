from django.contrib import admin

from .models import Profile, Plan


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
	list_display = ('user', 'website', 'created_at')


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
	list_display = ('title', 'created_at')
	prepopulated_fields = {"slug": ("title",)}
