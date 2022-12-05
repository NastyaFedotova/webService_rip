from .models import Ticket, Event, User
from rest_framework import serializers


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket

        fields = ['id_ticket', 'id_event', 'id_user', 'amount', 'date_of_buying', 'booking_date', 'ticket_status']

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event

        fields = ['id_event', 'name', 'price', 'description', 'date_event', 'duration', 'img']