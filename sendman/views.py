from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import TemplateView
from django_celery_beat.models import PeriodicTask, CrontabSchedule
import json

from .forms import *
from .tasks import *
from .models import *


class Sendman(TemplateView):
    template_name = "sendman/sender.html"

    def dispatch(self, request, *args, **kwargs):
        templates = Template.objects.all()
        recipients = SubscriberList.objects.all()
        intervals = CrontabSchedule.objects.all()

        schedules = []
        for i in intervals:
            schedules.append((i.id, i))

        context = {
            "recipients": recipients,
            "templates": templates,
            "schedules": schedules
        }

        # simple form
        if request.method == 'POST':
            # form = SendForm(request.POST)  # + request.FILES
            # if form.is_valid():

            tmpl = request.POST.get('template', None)
            rcpt_list = request.POST.get('recipients', None)
            repeat = request.POST.get('repeat', None)
            schedule = request.POST.get('schedulers', None)

            template = Template.objects.get(name=tmpl)
            recipients = SubscriberList.objects.get(name=rcpt_list)
            # recipient = Subscriber.objects.filter(list=rcpt.pk).values()

            if repeat:
                if not schedule:     #reconf
                    minute = "*" if not request.POST.get('minute') else request.POST.get('minute')
                    hour = "*" if not request.POST.get('hour') else request.POST.get('hour')
                    day_of_month = "*" if not request.POST.get('day_of_month') else request.POST.get('day_of_month')
                    month = "*" if not request.POST.get('month') else request.POST.get('month')
                    day_of_week = "*" if not request.POST.get('day_of_week') else request.POST.get('day_of_week')

                    # print(f"crontab:{minute} {hour} {day_of_month} {month} {day_of_week}")

                    schedule, created = CrontabSchedule.objects.get_or_create(
                        minute=minute,
                        hour=hour,
                        day_of_month=day_of_month,
                        month_of_year=month,
                        day_of_week=day_of_week,
                    )

                else:
                    id = int(schedule.split('(')[1].split(",")[0])
                    schedule = CrontabSchedule.objects.get(id=id)
                    # crontab == type of CrontabSchedule, not a string

                task = PeriodicTask.objects.create(
                    crontab=schedule,
                    name=f"crontab:{schedule}",
                    task='send_mail_task',
                    args=json.dumps([template.id, recipients.id])
                )

            else:
                send_mail_task.delay(template.id, recipients.id)
                SendHistory.objects.create(template=template, rcpt_list=recipients)

            # messages.success(request, "Рассылка успешно выполнена!")
            context['message'] = "Рассылка успешно выполнена!"

            return render(request, self.template_name, context)
        # else:
        #     form = SendForm()

        # context["form"] = form

        return render(request, self.template_name, context)


class ShowTemplates(TemplateView):
    template_name = "sendman/templates.html"

    def dispatch(self, request, *args, **kwargs):
        templates = Template.objects.all()

        context = {
            "templates": templates,
        }
        return render(request, self.template_name, context)


class NewTemplate(TemplateView):
    template_name = "sendman/new_template.html"

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = AddTemplateForm(request.POST, request.FILES)

            if form.is_valid():
                form.save()
                messages.success(request, "Макет добавлен!")
                return redirect(reverse("send_email"))
        else:
            form = AddTemplateForm()

        context = {
            "form": form
        }

        return render(request, self.template_name, context)


def deleteTemplate(request, pk):
    template_name = "sendman/templates.html"

    template = Template.objects.get(pk=pk)
    template.delete()

    templates = Template.objects.all()

    context = {
        "templates": templates,
    }
    return render(request, template_name, context)


class ShowHistory(TemplateView):
    template_name = "sendman/history.html"

    def dispatch(self, request, *args, **kwargs):
        history = SendHistory.objects.all()
        context = {
            "history": history
        }

        return render(request, self.template_name, context)


class ShowLists(TemplateView):
    template_name = "sendman/recipients.html"

    def dispatch(self, request, *args, **kwargs):
        recipients = SubscriberList.objects.all()

        context = {
            "recipients": recipients,
        }
        return render(request, self.template_name, context)


def showList(request, pk):
    template_name = "sendman/list.html"
    list = get_object_or_404(SubscriberList, pk=pk)

    if request.method == 'POST':
        form = AddSubscriberListForm(request.POST, instance=list)  # + request.FILES,

        list_name = request.POST.get('name', None)
        subscribers = request.POST.get('subscribers', None)

        number = 0

        if form.is_valid():
            form.save()

            list = SubscriberList.objects.get(name=list_name)
            subscriber_info = subscribers.split(';')

            for info in subscriber_info:
                name = info.split(' ')[0]
                surname = info.split(' ')[1]
                email = info.split(' ')[2]
                number = number + 1
                new = Subscriber.objects.get_or_create(name=name, surname=surname, email=email)    # отдает Tuple
                new[0].list.add(list)

            list.number = 0 if not number else number

            messages.success(request, "Список изменен!")
            return redirect(reverse("recipients"))

    else:
        form = AddSubscriberListForm(instance=list)    # initial => dict

    context = {
        "form": form
    }
    return render(request, template_name, context)


def newList(request):
    template_name = "sendman/list.html"
    list = None


    if request.method == 'POST':
        form = AddSubscriberListForm(request.POST)

        list_name = request.POST.get('name', None)
        subscribers = request.POST.get('subscribers', None)

        number = 0

        if form.is_valid():
            form.save()

            list = SubscriberList.objects.get(name=list_name)
            subscriber_info = subscribers.split(';')

            for info in subscriber_info:
                name = info.split(' ')[0]
                surname = info.split(' ')[1]
                email = info.split(' ')[2]
                number = number + 1
                new = Subscriber.objects.get_or_create(name=name, surname=surname, email=email)  # отдает Tuple
                new[0].list.add(list)

            list.number = 0 if not number else number

            messages.success(request, "Список создан!")
            return redirect(reverse("recipients"))

    else:
        form = AddSubscriberListForm()

    context = {
        "form": form
    }
    return render(request, template_name, context)


def deleteList(request, pk):
    template_name = "sendman/recipients.html"

    list = SubscriberList.objects.get(pk=pk)
    list.delete()

    recipients = SubscriberList.objects.all()

    context = {
        "recipients": recipients,
    }
    return render(request, template_name, context)






