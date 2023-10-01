from django.contrib import admin
from .models import Contact,Ringtone,WallpaperProposal
# Register your models here.
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'phone_number', 'user')

@admin.register(Ringtone)
class RingtoneAdmin(admin.ModelAdmin):
    list_display = ('id','ringtone_name', 'user', 'contact')

@admin.register(WallpaperProposal)
class WallpaperProposalAdmin(admin.ModelAdmin):
    list_display = ('id','proposer', 'contact', 'proposal_message')