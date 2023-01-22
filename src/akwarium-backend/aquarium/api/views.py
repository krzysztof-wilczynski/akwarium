from django.http import HttpResponse
from rest_framework import permissions
from rest_framework.views import APIView
from aquarium.models import Setpoint


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
