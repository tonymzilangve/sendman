from django import forms
from .tasks import *
from .models import *


class SendForm(forms.Form):
    template = forms.ModelChoiceField(queryset=Template.objects.all())
    recipients = forms.ModelChoiceField(queryset=SubscriberList.objects.all(), empty_label="Всем_подписчикам")


class AddTemplateForm(forms.ModelForm):
    class Meta:
        model = Template
        fields = "__all__"


class AddSubscriberListForm(forms.ModelForm):
    class Meta:
        model = SubscriberList
        exclude = ['number']


class AddSubscriberForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        exclude = ['list']

