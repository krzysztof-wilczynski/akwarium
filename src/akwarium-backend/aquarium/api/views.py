from django.http import HttpResponse, JsonResponse
from rest_framework import permissions
from rest_framework.views import APIView
from aquarium.models import Setpoint
from django_celery_beat.models import PeriodicTask


class UpdateSetpoints(APIView):
    permission_classes = [permissions.AllowAny]

    @staticmethod
    def post(request):
        data = request.data['data']

        for setpoint in data:
            sp_obj = Setpoint.objects.get(id=setpoint['id'])
            sp_obj.value = float(setpoint['value'])
            sp_obj.save()

        return HttpResponse(status=200)


class UpdateLightHours(APIView):
    permission_classes = [permissions.AllowAny]

    @staticmethod
    def get(request):
        light_on = PeriodicTask.objects.get(task="aquarium.tasks.switch_light", args="[0]")
        light_off = PeriodicTask.objects.get(task="aquarium.tasks.switch_light", args="[1]")

        time_on = f"{light_on.crontab.hour}:{light_on.crontab.minute}"
        time_off = f"{light_off.crontab.hour}:{light_off.crontab.minute}"

        return JsonResponse({"on": time_on, "off": time_off})

    @staticmethod
    def post(request):
        data = request.data['data']

        light_on = PeriodicTask.objects.get(task="aquarium.tasks.switch_light", args="[0]")
        light_off = PeriodicTask.objects.get(task="aquarium.tasks.switch_light", args="[1]")

        cron_on = light_on.crontab
        cron_off = light_off.crontab

        cron_on.hour, cron_on.minute = data['on'].split(':')
        cron_off.hour, cron_off.minute = data['off'].split(':')

        cron_on.save()
        cron_off.save()

        return HttpResponse(status=200)
