from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ContactViewSet,RingtoneViewSet,WallpaperProposalViewSet,ContactRingtoneUpdate,ContactWallpaperProposalUpdate,FilterWallpaperProposals,ContactsByCurrentUser,WallpaperProposalsByContact,WallpaperProposalDetail
from . import views

router = DefaultRouter()
router.register(r'contacts', ContactViewSet)
router.register(r'ringtones', RingtoneViewSet)
router.register(r'wallpaper-proposals', WallpaperProposalViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('contacts/<int:pk>/upload-image/', ContactViewSet.as_view(({'patch': 'update_contact_image'})), name='contact-image-update'),
    path('contacts/<int:contact_id>/update-ringtone/', ContactRingtoneUpdate.as_view(), name='update-contact-ringtone'),
    path('contacts/<int:contact_id>/update-wallpaper/', ContactWallpaperProposalUpdate.as_view(), name='update-contact-wallpaper'),
    path('profile/contacts/', ContactsByCurrentUser.as_view(), name='contacts-by-current-user'),
    path('profile/contacts/<int:contact_id>/wallpaper-proposed/', WallpaperProposalsByContact.as_view(), name='get-wallpaper-proposals-by-contact'),
    path('profile/contacts/<int:contact_id>/wallpaper-proposed/<int:wallpaper_id>/', WallpaperProposalDetail.as_view(), name='get-wallpaper-proposals-detail'),
    path('ringtones/<int:pk>/upload-ringtone/', RingtoneViewSet.as_view(({'patch':'upload_ringtone'})), name='ringtone-update'),
    path('wallpaper-proposals/<int:pk>/upload-wallpaper/', WallpaperProposalViewSet.as_view(({'patch':'upload_proposed_wallpaper'})), name='wallpaper-proposal-update'),
    path('wallpaper-proposals/my-proposals/', FilterWallpaperProposals.as_view(), name='filter-wallpaper-proposals'),
]
