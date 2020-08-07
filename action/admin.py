from django.contrib import admin

from .models import Action

@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    class Meta:
        ordering = ('-created')