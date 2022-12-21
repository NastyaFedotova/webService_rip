from django.contrib import admin

from .models import Event, Ticket, User

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'id', 'price')


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'id', 'email', 'is_superuser', 'is_staff')

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'status')