from django.contrib import admin
from app.models import *

admin.site.register(User)
admin.site.register(monitored_instance)
admin.site.register(moodle_heartbeat)
admin.site.register(alert)
admin.site.register(alert_rule)
