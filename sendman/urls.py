from django.urls import path
from .views import *

urlpatterns = [
    path('', Sendman.as_view(), name="send_email"),
    path('recipients', ShowLists.as_view(), name="recipients"),
    path('recipients/<int:pk>', showList, name="rcpt_list"),
    path('recipients/add', newList, name="new_recipients"),
    path('recipients/delete/<int:pk>', deleteList, name="delete_list"),

    path('template/new', NewTemplate.as_view(), name="new_template"),
    path('template/all', ShowTemplates.as_view(), name="templates"),
    path('template/delete/<int:pk>', deleteTemplate, name="delete_template"),
    path('history', ShowHistory.as_view(), name="history"),
]
