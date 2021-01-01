from django.contrib import admin

from counting.models import FinishPerDay


class FinishPerDayAdmin(admin.ModelAdmin):
    list_display = ("finish_time", "score", "spended_time")


admin.site.register(FinishPerDay, FinishPerDayAdmin)
