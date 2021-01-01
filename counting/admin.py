from django.contrib import admin

from counting.models import FinishPerDay, SiteConfiguration
from solo.admin import SingletonModelAdmin


class FinishPerDayAdmin(admin.ModelAdmin):
    list_display = ("finish_time", "score", "spended_time")


admin.site.enable_nav_sidebar = False


admin.site.register(FinishPerDay, FinishPerDayAdmin)
admin.site.register(SiteConfiguration, SingletonModelAdmin)
