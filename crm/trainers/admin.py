from django.contrib import admin
from .models import Client, Address, Team, Trainer, Activity, Abonement

admin.site.register(Activity)
admin.site.register(Client)
admin.site.register(Address)
admin.site.register(Team)
admin.site.register(Trainer)
admin.site.register(Abonement)