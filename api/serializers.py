from rest_framework import serializers
from .models import Event, Photographer, Assignment


class PhotographerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photographer
        fields = ['id', 'name', 'email', 'phone', 'is_active']


class EventSerializer(serializers.ModelSerializer):
    assigned_photographers = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = [
            'id', 'event_name', 'event_date', 'photographers_required',
            'created_at', 'assigned_photographers'
        ]

    def get_assigned_photographers(self, obj):
        assignments = obj.assignments.select_related('photographer').all()
        photographers = [a.photographer for a in assignments]
        return PhotographerSerializer(photographers, many=True).data


class SimpleEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            'id', 'event_name', 'event_date', 'photographers_required',
            'created_at'
        ]


class AssignmentSerializer(serializers.ModelSerializer):
    photographer = PhotographerSerializer(read_only=True)
    event = EventSerializer(read_only=True)

    class Meta:
        model = Assignment
        fields = ['id', 'event', 'photographer', 'assigned_at']
