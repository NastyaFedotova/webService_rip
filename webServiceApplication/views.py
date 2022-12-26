import uuid
import redis
from django.conf import settings
from django.db.models import Max, Min

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from .permissions import IsStaff, IsSuperUser
from .serializers import TicketSerializer, EventSerializer, RegistrationSerializer, LoginSerializer
from .models import Ticket, Event, User

session_storage = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)


class TicketViewSet(viewsets.ModelViewSet):
    serializer_class = TicketSerializer  # преобразование таблиц из БД в json

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'partial_update', 'create' ,'post', 'destroy']:
            #permission_classes = [IsAuthenticatedOrReadOnly]
            permission_classes = [AllowAny]
        elif self.action in ['update']:
            permission_classes = [IsStaff]
        else:
            permission_classes = [IsSuperUser]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = Ticket.objects.all()
        user_id = self.request.query_params.get('user_id')
        ticket_status = self.request.query_params.get('ticket_status')
        if ticket_status:
            queryset = queryset.filter(status=ticket_status)
        if user_id:
            queryset = queryset.filter(user=user_id)
        return queryset

    def list(self, request, *args, **kwargs):
        serializer = TicketSerializer(self.get_queryset(), many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, **kwargs):
        queryset = Ticket.objects.all()
        ticket = get_object_or_404(queryset, pk=pk)
        serializer = TicketSerializer(ticket)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        request_ticket = request.data
        ticket_serialized = TicketSerializer(request_ticket)
        request_ticket.save()
        return Response(ticket_serialized.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None, **kwargs):
        try:
            ticket = Ticket.objects.get(pk=pk)
        except Ticket.DoesNotExist:
            return Response({'message': 'The tickets does not exist'}, status=status.HTTP_404_NOT_FOUND)
        serializer = TicketSerializer(ticket, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None, **kwargs):
        try:
            ticket = Ticket.objects.get(pk=pk)
        except Ticket.DoesNotExist:
            return Response({'message': 'The tickets does not exist'}, status=status.HTTP_404_NOT_FOUND)
        serializer = TicketSerializer(ticket, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None, **kwargs):
        try:
            ticket = Ticket.objects.get(pk=pk)
            serializer = TicketSerializer(ticket)
            ticket.delete()
        except Exception:
            return Response(self.serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_200_OK)


class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'partial_update', 'price_range']:
            # permission_classes = [IsAuthenticatedOrReadOnly]
            permission_classes = [AllowAny]
        elif self.action in ['create', 'update', 'destroy']:
            permission_classes = [IsStaff]
        else:
            permission_classes = [IsSuperUser]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = Event.objects.all()
        event_ids = self.request.query_params.get('event_ids')
        name = self.request.query_params.get('name')
        price_min = self.request.query_params.get('price_min')
        price_max = self.request.query_params.get('price_max')
        date_start = self.request.query_params.get('date_start')
        date_end = self.request.query_params.get('date_end')
        date = self.request.query_params.get('date')
        duration_min = self.request.query_params.get('duration_min')
        duration_max = self.request.query_params.get('duration_max')

        if event_ids:
            queryset = queryset.filter(id__in=event_ids.split(','))
        if name:
            queryset = queryset.filter(title__contains=name)
        if price_min:
            queryset = queryset.filter(price__gte=price_min)
        if price_max:
            queryset = queryset.filter(price__lte=price_max)
        if date_start:
            queryset = queryset.filter(event_date__gte=date_start)
        if date_end:
            queryset = queryset.filter(event_date__lte=date_end)
        if date:
            queryset = queryset.filter(event_date__startswith=date)
        if duration_min:
            queryset = queryset.filter(duration__gte=duration_min)
        if duration_max:
            queryset = queryset.filter(duration__lte=duration_max)
        return queryset

    @action(detail=False, methods=['get'])
    def price_range(self, request):
        events = self.get_queryset()
        try:
            return Response(events.aggregate(price_min=Min('price'), price_max=Max('price')))
        except:
            return Response([], status=status.HTTP_404_NOT_FOUND)

    def list(self, request, *args, **kwargs):
        serializer = EventSerializer(self.get_queryset(), many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, **kwargs):
        queryset = Event.objects.all()
        event = get_object_or_404(queryset, pk=pk)
        serializer = EventSerializer(event)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        request_event = request.data
        event_serialized = EventSerializer(request_event)
        request_event.save()
        return Response(event_serialized.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None, **kwargs):
        try:
            event = Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            return Response({'message': 'The events does not exist'}, status=status.HTTP_404_NOT_FOUND)
        serializer = EventSerializer(event, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None, **kwargs):
        try:
            event = Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            return Response({'message': 'The events does not exist'}, status=status.HTTP_404_NOT_FOUND)
        serializer = EventSerializer(event, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None, **kwargs):
        try:
            event = Event.objects.get(pk=pk)
            serializer = EventSerializer(event)
            Event.objects.get(pk=pk).delete()
        except Exception:
            return Response(self.serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            response = Response(serializer.data, status=status.HTTP_200_OK)
            user = User.objects.get(username=serializer.data.get('username'))
            random_key = str(uuid.uuid4())
            response.set_cookie(key='session_id', value=random_key, samesite='None', secure=True)
            session_storage.set(random_key, value=user.pk)
            return response
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


class RegistrationAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"status": "registration successful"}, status=status.HTTP_201_CREATED)


class LogoutAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        session_id = request.COOKIES.get('session_id')
        if session_id:
            session_storage.delete(session_id)
            response = Response({"status": "logout"}, status=status.HTTP_200_OK)
            response.delete_cookie('session_id')
            return response

        return Response({"status": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
