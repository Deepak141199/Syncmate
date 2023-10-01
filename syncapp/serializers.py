from rest_framework import serializers
from .models import Contact, Ringtone, WallpaperProposal

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'

class RingtoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ringtone
        fields = '__all__'

class WallpaperProposalSerializer(serializers.ModelSerializer):
    contact_name = serializers.ReadOnlyField(source='contact.name')
    proposer_contact_id = serializers.PrimaryKeyRelatedField(queryset=Contact.objects.all(), source='proposer',write_only=True)
    proposer_name = serializers.ReadOnlyField(source='proposer.username')
    class Meta:
        model = WallpaperProposal
        fields = '__all__'
