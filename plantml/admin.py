from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Disease, Message, Review, Subscriber, TeamMember

# Register your models here.

class DiseaseAdmin(admin.ModelAdmin):
    list_display = ['plant_name', 'disease_name', 'date_created', 'last_modified']

class MessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone']

admin.site.register(Disease, DiseaseAdmin)
admin.site.register(TeamMember)
admin.site.register(Message, MessageAdmin)
admin.site.register(Review)
admin.site.register(Subscriber)

admin.site.unregister(Group)