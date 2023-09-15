from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from meetmaybeserverapi.models import Location
from meetmaybeserverapi.models import LocationType
from meetmaybeserverapi.models import Attendee

class LocationView(ViewSet):
    
    def retrieve(self, request, pk):
        
        try:
            location_type = Location.objects.get(pk=pk)
            serializer = LocationSerializer(location_type)
            return Response(serializer.data)
        except Location.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


    def list(self, request):
        
        locations = Location.objects.all()
        
        location_type = request.query_params.get('type', None)
        if location_type is not None:
            locations = locations.filter(location_type=location_type)
            
        serializer = LocationSerializer(locations, many=True)
        return Response(serializer.data)
    
    def create(self, request):
    	
        attendee = Attendee.objects.get(pk=request.data["attendee"])
        location_type = LocationType.objects.get(pk=request.data["locationType"])
        
        location = Location.objects.create(
            name=request.data["name"],
			address=request.data["address"],
			hours=request.data["hours"],
   			attendee=attendee,
			location_type=location_type,
		)
        serializer = LocationSerializer(location)
        return Response(serializer.data)
    
    def update(self, request, pk):
        """Handle PUT requests for a location
        """

        location = Location.objects.get(pk=pk)
        location.name = request.data["name"]
        location.address = request.data["address"]
        location.hours = request.data["hours"]
        
        attendee = Attendee.objects.get(pk=request.data)
        location_type = LocationType.objects.get(pk=request.data["locationType"])
        location.attendee = attendee
        location.location_type = location_type
        location.save()

        serializer = LocationSerializer(location)
        return Response(serializer.data)
    
    def destroy(self, request, pk):
        
        location = Location.objects.get(pk=pk)
        location.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
        

class LocationSerializer(serializers.ModelSerializer):
    """JSON serializer for locations
    """
    class Meta:
        model = Location
        fields = ('id', 'name', 'address', 'hours', 'attendee', 'location_type')
        depth = 1
