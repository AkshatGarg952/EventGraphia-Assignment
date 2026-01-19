from rest_framework import viewsets, status
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction

from .models import Event, Photographer, Assignment
from .serializers import EventSerializer, PhotographerSerializer, SimpleEventSerializer
import datetime


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    @action(detail=True, methods=['post'], url_path='assign-photographers')
    def assign_photographers(self, request, pk=None):
        """
        Smart algorithm to assign photographers to an event.
        Ensures availability and requirements are met.
        """
        event = self.get_object()

        if event.event_date < datetime.date.today():
             raise ValidationError({"error": "Cannot assign photographers to past events."})

        if event.assignments.exists():
             raise ValidationError({"error": "Photographers are already assigned to this event."})

        required_count = event.photographers_required
        if required_count <= 0:
             raise ValidationError({"error": "Photographers required must be greater than 0."})

        busy_photographer_ids = Assignment.objects.filter(
            event__event_date=event.event_date
        ).values_list('photographer_id', flat=True)

        available_photographers = Photographer.objects.filter(
            is_active=True
        ).exclude(
            id__in=busy_photographer_ids
        )

        if available_photographers.count() < required_count:
             raise ValidationError({
                "error": "Not enough available photographers for this date.",
                "required": required_count,
                 "available": available_photographers.count()
             })

        selected_photographers = available_photographers[:required_count]

        with transaction.atomic():
            assignments = []
            for photographer in selected_photographers:
                assignments.append(
                    Assignment(event=event, photographer=photographer)
                )
            Assignment.objects.bulk_create(assignments)

        serializer = PhotographerSerializer(selected_photographers, many=True)
        return Response(
            {
                "message": "Photographers assigned successfully.",
                "assigned_photographers": serializer.data
            },
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['get'])
    def assignments(self, request, pk=None):
        """
        Get all photographers assigned to the event.
        """
        event = self.get_object()
        assignments = event.assignments.all()

        photographers = [a.photographer for a in assignments]
        serializer = PhotographerSerializer(photographers, many=True)
        return Response(serializer.data)


class PhotographerViewSet(viewsets.ModelViewSet):
    queryset = Photographer.objects.all()
    serializer_class = PhotographerSerializer

    @action(detail=True, methods=['get'])
    def schedule(self, request, pk=None):
        """
        Get all events assigned to this photographer.
        """
        photographer = self.get_object()
        assignments = photographer.assignments.select_related('event').all()
        events = [a.event for a in assignments]
        serializer = SimpleEventSerializer(events, many=True)
        return Response(serializer.data)
