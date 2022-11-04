from rest_framework import viewsets
from .serializers import TicketSerializer, EventSerializer
from .models import Ticket, Event
from rest_framework.decorators import api_view, renderer_classes
from rest_framework import response, schemas
from rest_framework_swagger.renderers import OpenAPIRenderer, SwaggerUIRenderer


@api_view()
@renderer_classes([OpenAPIRenderer, SwaggerUIRenderer])
def schema_view(request):
    generator = schemas.SchemaGenerator(title='Bookings API')
    return response.Response(generator.get_schema(request=request))

class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all().order_by('id_ticket')
    serializer_class = TicketSerializer

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all().order_by('id_event')
    serializer_class = EventSerializer