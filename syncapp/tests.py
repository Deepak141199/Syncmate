from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from rest_framework.authtoken.models import Token
from django.core.files.uploadedfile import SimpleUploadedFile 
from .models import User,WallpaperProposal,Ringtone,Contact

#models
class ContactModelTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_create_contact(self):
        # Create a test image file
        image = SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg")

        contact = Contact.objects.create(
            user=self.user,
            name='Test Contact',
            phone_number='1234567890',
            contact_image=image,  # Assign the test image
        )

        self.assertEqual(contact.user, self.user)
        self.assertEqual(contact.name, 'Test Contact')
        self.assertEqual(contact.phone_number, '1234567890')

class RingtoneModelTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_create_ringtone(self):
        # Create a test ringtone file
        ringtone_file = SimpleUploadedFile("test_ringtone.mp3", b"file_content", content_type="audio/mpeg")

        # Create a contact for the ringtone
        contact = Contact.objects.create(
            user=self.user,
            name='Test Contact',
            phone_number='1234567890',
        )

        ringtone = Ringtone.objects.create(
            user=self.user,
            contact=contact,
            ringtone_name='Test Ringtone',
            ringtone_file=ringtone_file,  # Assign the test ringtone file
        )

        self.assertEqual(ringtone.user, self.user)
        self.assertEqual(ringtone.contact, contact)
        self.assertEqual(ringtone.ringtone_name, 'Test Ringtone')

class WallpaperProposalModelTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_create_wallpaper_proposal(self):
        # Create a test wallpaper file
        wallpaper_file = SimpleUploadedFile("test_wallpaper.jpg", b"file_content", content_type="image/jpeg")

        # Create a contact for the wallpaper proposal
        contact = Contact.objects.create(
            user=self.user,
            name='Test Contact',
            phone_number='1234567890',
        )

        wallpaper_proposal = WallpaperProposal.objects.create(
            proposer=self.user,
            contact=contact,
            proposed_wallpaper=wallpaper_file,  # Assign the test wallpaper file
            proposal_message='Test proposal message',
        )

        self.assertEqual(wallpaper_proposal.proposer, self.user)
        self.assertEqual(wallpaper_proposal.contact, contact)
        self.assertEqual(wallpaper_proposal.proposal_message, 'Test proposal message')


#views 

class ContactViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()  # Initialize the test client
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)  # Create a token for the user

        # Set the token in the client's headers for authentication
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_create_contact(self):
      data = {
        'user': self.user.id,
        'name': 'Test Contact',
        'phone_number': '1234567890',
    }
      response = self.client.post('/api/contacts/', data, format='json')
      self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_contacts(self):
      response = self.client.get('/api/contacts/')
      self.assertEqual(response.status_code, status.HTTP_200_OK)


