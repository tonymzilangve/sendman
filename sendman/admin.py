from django.contrib import admin
from .models import *


class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'surname', 'email')
    list_display_links = ('id', 'email')
    search_fields = ('name', 'surname', 'email')
    list_filter = ('email',)


class ListAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at')
    # list_display_links = ('name',)
    search_fields = ('name',)
    list_filter = ('name',)


class TemplateAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'subject')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'subject')


class SendHistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'template', 'rcpt_list', 'created_at', 'schedule')
    list_display_links = ('id', 'template', 'rcpt_list')
    search_fields = ('template', 'rcpt_list')
    list_filter = ('template', 'rcpt_list', )


admin.site.register(Subscriber, SubscriberAdmin)
admin.site.register(SubscriberList, ListAdmin)
admin.site.register(Template, TemplateAdmin)
admin.site.register(SendHistory, SendHistoryAdmin)
