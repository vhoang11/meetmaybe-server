from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from meetmaybeserverapi.models import EventAttendee, Attendee, Event

class EventAttendeeView(ViewSet):

    def retrieve(self, request, pk):
        
        try:
            event_attendee = EventAttendee.objects.get(pk=pk)
            serializer = EventAttendeeSerializer(event_attendee)
            return Response(serializer.data)
        except EventAttendee.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        serializer = EventAttendeeSerializer(event_attendee)
        return Response(serializer.data)
    
    def list(self, request):
        
        event_attendees = EventAttendee.objects.all()
        
        event_attendee = request.query_params.get('attendee', None)
        if event_attendee is not None:
            event_attendees = event_attendees.filter(event_attendee=event_attendee)
            
        """Filters by event id"""
        event_id = request.query_params.get('event_id', None)
        if event_id is not None:
            event_attendees = event_attendees.filter(event=event_id)
            
        serializer = EventAttendeeSerializer(event_attendees, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        
        attendee = Attendee.objects.get(pk=request.data["attendee"])
        event = Event.objects.get(pk=request.data["event"])
        
        event_attendee = EventAttendee.objects.create(
   			attendee=attendee,
			event=event,
		)
        serializer = EventAttendeeSerializer(event_attendee)
        return Response(serializer.data)
    
    def update(self, request, pk):
        """Handle PUT requests for an event

        Returns:
            Response -- Empty body with 204 status code
        """
        
        event_attendee = EventAttendee.objects.get(pk=pk)
        
        attendee = Attendee.objects.get(pk=request.data)
        event = Event.objects.get(pk=request.data["event"])
        event_attendee.attendee = attendee
        event_attendee.event = event
        event_attendee.save()

        serializer = EventAttendeeSerializer(event_attendee)
        return Response(serializer.data)
    
    def destroy(self, request, pk):
        
        event_attendee = EventAttendee.objects.get(pk=pk)
        event_attendee.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
        


class EventAttendeeSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """
    class Meta:
        model = EventAttendee
        fields = ('id', 'attendee', 'event')
        depth = 2
