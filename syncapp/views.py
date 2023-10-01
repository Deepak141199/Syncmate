from django.shortcuts import render
from rest_framework import viewsets
from django.views.decorators.csrf import csrf_exempt
from .models import Contact, Ringtone, WallpaperProposal
from .serializers import ContactSerializer, RingtoneSerializer, WallpaperProposalSerializer,ContactWithoutUserSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.decorators import api_view, permission_classes
from .permissions import mypermission
from rest_framework import generics
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated

# Create your views here.

#@csrf_exempt
class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated,mypermission]  # only authenticated users


    def get_queryset(self):
        user = self.request.user    # Get the user associated with the token in the headers
        return Contact.objects.filter(user=user)
    


    @action(detail=True, methods=['PATCH'])
    def update_contact_image(self , request, pk=None):
        try:
            contact = Contact.objects.get(pk=pk)
        except Contact.DoesNotExist:
            return Response({'error': 'Contact not found'}, status=status.HTTP_404_NOT_FOUND,)

    # Check if the user has permission to update this contact (e.g., if it's their own contact)
        if contact.user != request.user:
          return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

    # Update the contact's image
        contact.contact_image = request.data.get('contact_image')
        contact.save()

        serializer = ContactSerializer(contact)
        return Response(serializer.data, status=status.HTTP_200_OK)




class ContactRingtoneUpdate(APIView):
    permission_classes = [IsAuthenticated, mypermission]
    def patch(self, request, contact_id):
        try:
            contact = Contact.objects.get(pk=contact_id)
        except Contact.DoesNotExist:
            return Response({'error': 'Contact not found'}, status=status.HTTP_404_NOT_FOUND)

        # Check if the user has permission to update this contact (e.g., if it's their own contact)
        if contact.user != request.user:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
                # Get the related Ringtone object for the contact
        try:
            ringtone = Ringtone.objects.get(contact=contact)
        except Ringtone.DoesNotExist:
            return Response({'error': 'Ringtone not found'}, status=status.HTTP_404_NOT_FOUND)

        # Update the RingtoneSerializer with the request data
        serializer = RingtoneSerializer(ringtone, data=request.data, partial=True)

        if serializer.is_valid():
            # Save the updated Ringtone object
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ContactWallpaperProposalUpdate(APIView):
    def patch(self, request, contact_id):
        try:
            contact = Contact.objects.get(pk=contact_id)
        except Contact.DoesNotExist:
            return Response({'error': 'Contact not found'}, status=status.HTTP_404_NOT_FOUND)

        # Check if the user has permission to update this contact (e.g., if it's their own contact)
        if contact.user != request.user:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

        # Get the related WallpaperProposal object for the contact
        try:
            wallpaper_proposal = WallpaperProposal.objects.get(contact=contact)
        except WallpaperProposal.DoesNotExist:
            return Response({'error': 'Wallpaper Proposal not found'}, status=status.HTTP_404_NOT_FOUND)

        # Update the WallpaperProposalSerializer with the request data
        serializer = WallpaperProposalSerializer(wallpaper_proposal, data=request.data, partial=True)

        if serializer.is_valid():
            # Save the updated WallpaperProposal object
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)







#contact details by current user

class ContactsByCurrentUser(generics.ListAPIView):
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Get the currently logged-in user from the request
        current_user = self.request.user

        # Filter the contacts based on the user's name
        queryset = Contact.objects.filter(name=current_user.username)

        return queryset









###########################################################################################################

class RingtoneViewSet(viewsets.ModelViewSet):
    queryset = Ringtone.objects.all()
    serializer_class = RingtoneSerializer
    permission_classes = [IsAuthenticated,mypermission]  

    def get_queryset(self):
        user = self.request.user
        return Ringtone.objects.filter(user=user)
    

    @action(detail=True, methods=['PATCH'])
    def upload_ringtone(self, request, pk):
      try:
         ringtone = Ringtone.objects.get(pk=pk)
      except Ringtone.DoesNotExist:
        return Response({'error': 'Ringtone not found'}, status=status.HTTP_404_NOT_FOUND)

    # Check if the user has permission to update this ringtone (e.g., if it's their own ringtone)
      if ringtone.user != request.user:
        return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

    # Update the ringtone's file
      ringtone.ringtone_file = request.data.get('ringtone_file')
      ringtone.save()

      serializer = RingtoneSerializer(ringtone)
      return Response(serializer.data, status=status.HTTP_200_OK)


##########################################################################################################3


class WallpaperProposalViewSet(viewsets.ModelViewSet):
    queryset = WallpaperProposal.objects.all()
    serializer_class = WallpaperProposalSerializer
    permission_classes = [IsAuthenticated,mypermission]  

    def get_queryset(self):
        user = self.request.user
        return WallpaperProposal.objects.filter(proposer=user)
    

    





    @action(detail=True, methods=['PATCH'])
    def upload_proposed_wallpaper(self, request, pk):
      try:
        proposed_wallpaper = WallpaperProposal.objects.get(pk=pk)
      except WallpaperProposal.DoesNotExist:
        return Response({'error': 'Proposed wallpaper not found'}, status=status.HTTP_404_NOT_FOUND)

    # Check if the user has permission to update this proposed wallpaper (e.g., if it's their own proposal)
      if proposed_wallpaper.proposer != request.user:
        return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

    # Update the proposed wallpaper's image
      proposed_wallpaper.proposed_wallpaper = request.data.get('proposed_wallpaper')
      proposed_wallpaper.save()

      serializer = WallpaperProposalSerializer(proposed_wallpaper)
      return Response(serializer.data, status=status.HTTP_200_OK)



#####################################################################################################

class FilterWallpaperProposals(APIView):
    queryset = WallpaperProposal.objects.all()
    serializer_class = WallpaperProposalSerializer
    permission_classes = [IsAuthenticated, mypermission]

    def get(self):
        user= self.request.user  # Get the ID of the logged-in user

        try:
            proposals = WallpaperProposal.objects.filter(contact=user)
            serializer = WallpaperProposalSerializer(proposals, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except WallpaperProposal.DoesNotExist:
            return Response({'error': 'No matching wallpaper proposals found'}, status=status.HTTP_404_NOT_FOUND)

###############################################################################################################

class WallpaperProposalsByContact(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, contact_id):
        try:
            wallpaper_proposals = WallpaperProposal.objects.filter(contact__id=contact_id)
            serializer = WallpaperProposalSerializer(wallpaper_proposals, many=True)
            return Response(serializer.data)
        except WallpaperProposal.DoesNotExist:
            return Response({'message': 'No wallpaper proposals found for this contact.'}, status=status.HTTP_404_NOT_FOUND)
        


#############################  specific proposal  #########################################################
class WallpaperProposalDetail(APIView):
    def get(self, request, contact_id, wallpaper_id):
        try:
            # Retrieve the specific wallpaper proposal by ID
            wallpaper_proposal = WallpaperProposal.objects.get(pk=wallpaper_id, contact_id=contact_id)
        except WallpaperProposal.DoesNotExist:
            return Response({'message': 'Wallpaper proposal not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Serialize the wallpaper proposal data
        serializer = WallpaperProposalSerializer(wallpaper_proposal)

        return Response(serializer.data, status=status.HTTP_200_OK)
    


    @action(detail=True, methods=['POST'])
    def post(self, request, contact_id, wallpaper_id):
      try:
        # Retrieve the specific wallpaper proposal by ID
        wallpaper_proposal = WallpaperProposal.objects.get(pk=wallpaper_id, contact_id=contact_id)
      except WallpaperProposal.DoesNotExist:
        return Response({'message': 'Wallpaper proposal not found.'}, status=status.HTTP_404_NOT_FOUND)

      action = request.data.get('action')  # Assuming you send 'action' in the request data.
      if action == 'accept':
        # Update the contact's image with the proposed wallpaper
        contact_id = wallpaper_proposal.contact_id  # Retrieve the contact ID from the WallpaperProposal
        try:
            contact = Contact.objects.get(pk=contact_id)
            contact.contact_image = wallpaper_proposal.proposed_wallpaper
            contact.save()
        except Contact.DoesNotExist:
            return Response({'message': 'Contact not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Update the proposal message in WallpaperProposal to indicate acceptance
        wallpaper_proposal.is_accepted = True
        wallpaper_proposal.save()

        return Response({'message': 'Wallpaper proposal accepted.'}, status=status.HTTP_200_OK)
      elif action == 'reject':
            # Delete the wallpaper proposal
            wallpaper_proposal.delete()
            return Response({'message': 'Wallpaper proposal rejected and deleted.'}, status=status.HTTP_200_OK)
      else:
            return Response({'message': 'Invalid action.'}, status=status.HTTP_400_BAD_REQUEST)
        




###################################################################################################################

class OwnContactDetailView(generics.RetrieveAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactWithoutUserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Get the logged-in user
        user = self.request.user

        # Filter the Contact objects based on the user's username
        contact = Contact.objects.filter(name=user.username).first()

        return contact