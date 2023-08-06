from django.contrib.admin import site, ModelAdmin
from grimoire.django.tracked.admin import CreatePeriodAgoAndCurrentFilter, UpdatePeriodAgoAndCurrentFilter
from .models import SampleRecord


class SampleAdmin(ModelAdmin):

    list_filter = (CreatePeriodAgoAndCurrentFilter, UpdatePeriodAgoAndCurrentFilter)
    list_display = ('id', 'content', 'created_on', 'updated_on')


site.register(SampleRecord, SampleAdmin)