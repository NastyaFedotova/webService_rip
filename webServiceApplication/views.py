from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import TicketSerializer, EventSerializer, UserSerializer
from .models import Ticket, Event, User
from django.db.models import Max, Min


class TicketViewSet(viewsets.ModelViewSet):
    serializer_class = TicketSerializer  # преобразование таблиц из БД в json

    def get_queryset(self):
        queryset = Ticket.objects.all()
        user_id = self.request.query_params.get('user_id')
        ticket_status = self.request.query_params.get('ticket_status')
        if ticket_status:
            queryset = queryset.filter(ticket_status=ticket_status)
        if user_id:
            queryset = queryset.filter(id_user__id_user=user_id)
        return queryset


@api_view(['GET'])
def priceRange(request):
    return Response(Event.objects.aggregate(price_min=Min('price'), price_max=Max('price')))


class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer

    def get_queryset(self):
        queryset = Event.objects.all()
        name = self.request.query_params.get('name')
        price_min = self.request.query_params.get('price_min')
        price_max = self.request.query_params.get('price_max')
        date_start = self.request.query_params.get('date_start')
        date_end = self.request.query_params.get('date_end')
        date = self.request.query_params.get('date')
        duration_min = self.request.query_params.get('duration_min')
        duration_max = self.request.query_params.get('duration_max')

        if name:
            queryset = queryset.filter(name__contains=name)
        if price_min:
            queryset = queryset.filter(price__gte=price_min)
        if price_max:
            queryset = queryset.filter(price__lte=price_max)
        if date_start:
            queryset = queryset.filter(date_event__gte=date_start)
        if date_end:
            queryset = queryset.filter(date_event__lte=date_end)
        if date:
            queryset = queryset.filter(date_event__startswith=date)
        if duration_min:
            queryset = queryset.filter(duration__gte=duration_min)
        if duration_max:
            queryset = queryset.filter(duration__lte=duration_max)
        return queryset


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer  # преобразование таблиц из БД в json
