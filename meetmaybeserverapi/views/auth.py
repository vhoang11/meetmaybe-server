from meetmaybeserverapi.models import Attendee
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['POST'])
def check_user(request):
    '''Checks to see if User has Associated Gamer

    Method arguments:
      request -- The full HTTP request object
    '''
    uid = request.data['uid']

    # Use the built-in authenticate method to verify
    # authenticate returns the user object or None if no user is found
    attendee = Attendee.objects.filter(uid=uid).first()

    # If authentication was successful, respond with their token
    if attendee is not None:
        data = {
            'id': attendee.id,
            'name': attendee.name,
            'username': attendee.username,
            'email': attendee.email,
            'profile_image_url': attendee.profile_image_url,
            'bio': attendee.bio,
            'uid': attendee.uid,
        }
        return Response(data)
    else:
        # Bad login details were provided. So we can't log the user in.
        data = { 'valid': False }
        return Response(data)


@api_view(['POST'])
def register_user(request):
    '''Handles the creation of a new attendee for authentication

    Method arguments:
      request -- The full HTTP request object
    '''

    # Now save the user info in the meetmaybeserverapi_attendee table
    attendee = Attendee.objects.create(
        name=request.data['name'],
        username=request.data['username'],
        email=request.data['email'],
        profile_image_url=request.data['profile_image_url'],
        bio=request.data['bio'],
        uid=request.data['uid']
    )

    # Return the attendee info to the client
    data = {
        'id': attendee.id,
        'name': attendee.name,
        'username': attendee.username,
        'email': attendee.email,
        'profile_image_url': attendee.profile_image_url,
        'bio': attendee.bio,
        'uid': attendee.uid,
    }
    return Response(data)
