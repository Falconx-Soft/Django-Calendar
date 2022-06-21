from dataclasses import fields
from pyexpat import model
from rest_framework import serializers
from .models import *

class EventSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Event
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    """
    Because 'snippets' is a reverse relationship on the User model,
    it will not be included by default when using the ModelSerializer class,
    so we needed to add an explicit field for it.
    """
    Event = serializers.PrimaryKeyRelatedField(many=True,queryset=Event.objects.all())

    class Meta:
        module = User
        fields = ('id', 'username', 'Event')