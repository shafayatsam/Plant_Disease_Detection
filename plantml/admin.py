from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Disease, Message, Review, Subscriber, TeamMember

# Register your models here.

class DiseaseAdmin(admin.ModelAdmin):
    list_display = ['plant_name', 'disease_name', 'date_created', 'last_modified']

class MessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'msg' , 'msg_dt']

class SubscriberAdmin(admin.ModelAdmin):
    list_display = ['username', 'email']

class ReviewAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'comment', 'review_dt']

admin.site.register(Disease, DiseaseAdmin)
admin.site.register(TeamMember)
admin.site.register(Message, MessageAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Subscriber, SubscriberAdmin)

admin.site.unregister(Group)