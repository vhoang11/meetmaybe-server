from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from meetmaybeserverapi.models import LocationType

class LocationTypeView(ViewSet):

    def retrieve(self, request, pk):
        
        try:
            location_type = LocationType.objects.get(pk=pk)
            serializer = LocationTypeSerializer(location_type)
            return Response(serializer.data)
        except LocationType.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        serializer = LocationTypeSerializer(location_type)
        return Response(serializer.data)
    
    def list(self, request):
        
        location_types = LocationType.objects.all()
        
        location_type = request.query_params.get('type', None)
        if location_type is not None:
            location_types = location_types.filter(location_type=location_type)
            
        serializer = LocationTypeSerializer(location_types, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        
        location_type = LocationType.objects.create(
            label=request.data["label"],
			dress_code=request.data["dressCode"],
		)
        serializer = LocationTypeSerializer(location_type)
        return Response(serializer.data)
    
    def update(self, request, pk):
        """Handle PUT requests for a location type

        Returns:
            Response -- Empty body with 204 status code
        """
        
        location_type = LocationType.objects.get(pk=pk)
        location_type.label = request.data["label"]
        location_type.dress_code = request.data["dressCode"]
        location_type.save()

        serializer = LocationTypeSerializer(location_type)
        return Response(serializer.data)
    
    def destroy(self, request, pk):
        
        location_type = LocationType.objects.get(pk=pk)
        location_type.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
        


class LocationTypeSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """
    class Meta:
        model = LocationType
        fields = ('id', 'label', 'dress_code')
        depth = 1
