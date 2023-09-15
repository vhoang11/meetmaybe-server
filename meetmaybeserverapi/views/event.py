"""View module for handling requests about event types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from meetmaybeserverapi.models import Event
from meetmaybeserverapi.models import Attendee
from meetmaybeserverapi.models import EventAttendee
from rest_framework.decorators import action

class EventView(ViewSet):
    """Level up events view"""

    def retrieve(self, request, pk):
        
        # event = Event.objects.get(pk=pk)
        try:
            event = Event.objects.get(pk=pk)
            serializer = EventSerializer(event)
            return Response(serializer.data)
        except Event.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        serializer = EventSerializer(event)
        return Response(serializer.data)

    def list(self, request):
        
        events = Event.objects.all()
        
        is_public = request.query_params.get('is_public', True)
        
        # Check if the 'is_public' query parameter is set to a truthy value (e.g., 'true' or '1')
        if is_public in ['true', '1']:
            events = Event.objects.filter(is_public=True)
            
        # uid = request.META['HTTP_AUTHORIZATION']
        # attendee = Attendee.objects.get(pk=pk)

        # for event in events:
            # Check to see if there is a row in the Event Locations table that has the passed in attendee and event
            # event.joined = len(EventAttendee.objects.filter(
            #     attendee=attendee, event=event)) > 0

            
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)
    
    def create(self, request):
    	
        organizer = Attendee.objects.get(pk=request.data["organizer"])
        invitee = Attendee.objects.get(pk=request.data["invitee"])
        
        event = Event.objects.create(
			title=request.data["title"],
			image_url=request.data["image_url"],
			description=request.data["description"],
			location=request.data["location"],
			date=request.data["date"],
			time=request.data["time"],
			organizer=organizer,
            invitee=invitee,
			is_public=request.data["is_public"],
			organizer_canceled=request.data["organizer_canceled"],
			invitee_canceled=request.data["invitee_canceled"]
        )
        serializer = EventSerializer(event)
        return Response(serializer.data)
    
    def update(self, request, pk):
        """Handle PUT requests for an event

        Returns:
            Response -- Empty body with 204 status code
        """

        event = Event.objects.get(pk=pk)
        event.title = request.data["title"]
        event.image_url = request.data["image_url"]
        event.description = request.data["description"]
        event.location = request.data["location"]
        event.date = request.data["date"]
        event.time = request.data["time"]
        event.is_public = request.data["is_public"]
        event.organizer_canceled = request.data["organizer_canceled"]
        event.invitee_canceled = request.data["invitee_canceled"]
        organizer = Attendee.objects.get(pk=request.data["organizer"])
        invitee = Attendee.objects.get(pk=request.data["invitee"])
        event.organizer = organizer
        event.invitee = invitee

        event.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk):
        
        event = Event.objects.get(pk=pk)
        event.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
        
    @action(methods=['post'], detail=True)
    def signup(self, request, pk):
        """Post request for a user to sign up for an event"""

        attendee = Attendee.objects.get(uid=request.META['HTTP_AUTHORIZATION'])
        event = Event.objects.get(pk=pk)
        attendee = EventAttendee.objects.create(
            attendee=attendee,
            event=event
        )
        return Response({'message': 'Attendee added'}, status=status.HTTP_201_CREATED)
    
    @action(methods=['delete'], detail=True)
    def leave(self, request, pk):
        """DELETE request for a user to sign up for an event"""

        attendee = Attendee.objects.get(uid=request.META['HTTP_AUTHORIZATION'])
        event = Event.objects.get(pk=pk)
        attendee = EventAttendee.objects.get(
            attendee=attendee,
            event=event
        )
        attendee.delete()
        return Response({'message': 'Attendee removed'}, status=status.HTTP_204_NO_CONTENT)

class EventSerializer(serializers.ModelSerializer):
    """JSON serializer for event types
    """
    class Meta:
        model = Event
        fields = ('id', 'title', 'image_url', 'description', 'location', 'date', 'time', 'organizer', 'invitee', 'is_public', 'organizer_canceled', 'invitee_canceled','joined')
        depth = 2
