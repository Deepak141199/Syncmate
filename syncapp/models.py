from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    contact_image = models.ImageField(upload_to='contact_images/', blank=True, null=True)

class Ringtone(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    ringtone_name = models.CharField(max_length=100)
    ringtone_file = models.FileField(upload_to='ringtones/')

class WallpaperProposal(models.Model):
    proposer = models.ForeignKey(User, on_delete=models.CASCADE)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    proposed_wallpaper = models.ImageField(upload_to='proposed_wallpapers/')
    proposal_message = models.TextField(blank=True, null=True)