from django.contrib.auth import authenticate

from .models import Ticket, Event, User
from rest_framework import serializers


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket

        fields = ['id', 'event', 'user', 'count', 'buying_date', 'booking_date', 'status']


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event

        fields = ['id', 'title', 'price', 'description', 'event_date', 'duration', 'img',
                  'place', 'latitude', 'longitude', 'address', 'remaining_tickets']


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(max_length=128, write_only=True)

    # Ignore these fields if they are included in the request.

    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField(read_only=True)
    is_worker = serializers.BooleanField(read_only=True)
    is_staff = serializers.BooleanField(read_only=True)
    is_superuser = serializers.BooleanField(read_only=True)

    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    birth_date = serializers.DateField(read_only=True)
    sex = serializers.CharField(read_only=True)

    def validate(self, data) -> User:
        username = data.get('username', None)
        password = data.get('password', None)

        if username is None:
            raise serializers.ValidationError(
                'A username address is required to log in.'
            )

        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )
        user = authenticate(username=username, password=password)
        if user is None:
            raise serializers.ValidationError(
                'A user with this username and password was not found.'
            )

        return user


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=4,
        write_only=True,
    )

    class Meta:
        model = User
        fields = (
            'id', 'email', 'first_name', 'last_name', 'username', 'password', 'is_staff', 'is_superuser',
            'personal_sale', 'status')

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
