from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from meetmaybeserverapi.models import Attendee

class AttendeeView(ViewSet):
    
    def retrieve(self, request, pk):
        
        try:
            attendee = Attendee.objects.get(pk=pk)
            serializer = AttendeeSerializer(attendee)
            return Response(serializer.data)
        except Attendee.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


    def list(self, request):
        
        attendees = Attendee.objects.all()
        
        username = request.query_params.get('type', None)
        if username is not None:
            attendees = attendees.filter(username=username)
        name = request.query_params.get('type', None)
        if name is not None:
            attendees = attendees.filter(name=name)
            
        serializer = AttendeeSerializer(attendees, many=True)
        return Response(serializer.data)
    
    def create(self, request):
    	
        # attendee = Attendee.objects.get(uid=request.data["name"])
        
        attendee = Attendee.objects.create(
			name=request.data["name"],
			username=request.data["username"],
			email=request.data["email"],
			profile_image_url=request.data["profileImageUrl"],
			bio=request.data["bio"],
			uid=request.data["uid"],
		)
        serializer = AttendeeSerializer(attendee)
        return Response(serializer.data)
    
    def update(self, request, pk):
        """Handle PUT requests for an attendee

        Returns:
            Response -- Empty body with 204 status code
        """

        attendee = Attendee.objects.get(pk=pk)
        attendee.name = request.data["name"]
        attendee.username = request.data["username"]
        attendee.email = request.data["email"]
        attendee.profile_image_url = request.data["profileImageUrl"]
        attendee.bio = request.data["bio"]
        attendee.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def search(self, request):
        """Search users by name, email, or username """

        name = request.query_params.get('name', None)
        email = request.query_params.get('email', None)
        username = request.query_params.get('username', None)
        bio = request.query_params.get('bio', None)

        attendee = Attendee.objects.all()

        if name:
            attendee = attendee.filter(name__icontains=name)
        if email:
            attendee = attendee.filter(email__icontains=email)
        if username:
            attendee = attendee.filter(username__icontains=username)

        serializer = AttendeeSerializer(attendee, many=True)
        return Response(serializer.data)

    def destroy(self, request, pk):
        
        attendee = Attendee.objects.get(pk=pk)
        attendee.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    
class AttendeeSerializer(serializers.ModelSerializer):
    """JSON serializer for event types
    """
    class Meta:
        model = Attendee
        fields = ('id', 'name', 'username', 'email', 'profile_image_url', 'bio', 'uid')
        depth = 1
