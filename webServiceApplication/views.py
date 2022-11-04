from rest_framework import viewsets
from .serializers import TicketSerializer, EventSerializer
from .models import Ticket, Event

class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all().order_by('id_ticket')
    serializer_class = TicketSerializer

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all().order_by('id_event')
    serializer_class = EventSerializer